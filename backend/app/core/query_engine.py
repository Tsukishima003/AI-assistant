"""Query engine for RAG system"""
import re
from typing import Dict, AsyncGenerator
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from app.core.prompts import RAG_PROMPT_TEMPLATE


def clean_citations(text: str) -> str:
    """Remove citation markers like 【1†L1-L9】"""
    return re.sub(r'【.*?】', '', text)


class QueryEngine:
    """Handles query processing and response generation"""
    
    def __init__(self, llm, vector_store, groq_api_key: str, model_name: str):
        self.llm = llm
        self.vector_store = vector_store
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        
        self.prompt = PromptTemplate(
            template=RAG_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        
        self.retriever = self.vector_store.as_retriever()
        self.retriever.search_kwargs = {"k": 4}
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.chain = create_retrieval_chain(self.retriever, self.document_chain)
    
    def query(self, question: str) -> Dict:
        result = self.chain.invoke({"input": question})
        sources = [doc.metadata.get('source', 'Unknown')
                   for doc in result.get('context', [])]
        return {
            "answer": clean_citations(result['answer']),
            "sources": list(set(sources))
        }
    
    async def query_stream(self, question: str) -> AsyncGenerator[Dict, None]:
        from app.core.llm import create_llm
        
        try:
            print(f"Starting query stream for: {question}")
            
            docs: list[Document] = self.retriever.invoke(question)
            print(f"Retrieved {len(docs)} documents")
            
            context = "\n\n".join([doc.page_content for doc in docs])
            prompt = self.prompt.format(context=context, question=question)
            
            streaming_llm = create_llm(
                api_key=self.groq_api_key,
                model_name=self.model_name,
                temperature=0.7,
                streaming=True
            )
            
            full_response = ""
            async for chunk in streaming_llm.astream(prompt):
                if hasattr(chunk, 'content') and chunk.content:
                    token = clean_citations(chunk.content)  # clean citations per token
                    full_response += token
                    yield {
                        "type": "token",
                        "content": token
                    }
            
            print(f"Streaming complete. Full response length: {len(full_response)}")
            
            # Fix: use "sources" key not "content"
            sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
            yield {
                "type": "sources",
                "sources": list(set(sources))  # ← fixed key
            }
            
            yield {
                "type": "done",
                "content": full_response
            }
            
        except Exception as e:
            print(f"Error in query_stream: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            yield {
                "type": "error",
                "content": f"{type(e).__name__}: {str(e)}"
            }