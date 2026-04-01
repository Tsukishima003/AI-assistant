"""Query engine for RAG system."""
import re
from typing import Dict, AsyncGenerator, Optional
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from app.core.prompts import RAG_PROMPT_TEMPLATE
from app.core.logging import get_logger

logger = get_logger(__name__)


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
            input_variables=["context", "question", "chat_history"]
        )
        
        self.retriever = self.vector_store.as_retriever()
        self.retriever.search_kwargs = {"k": 4}
    
    def query(self, question: str, chat_history: str = "") -> Dict:
        """Non-streaming query with optional chat history."""
        docs = self.retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])

        history_section = ""
        if chat_history:
            history_section = f"Previous conversation:\n{chat_history}\n"

        prompt_text = self.prompt.format(
            context=context,
            question=question,
            chat_history=history_section
        )

        result = self.llm.invoke(prompt_text)
        answer = clean_citations(result.content if hasattr(result, 'content') else str(result))

        sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
        return {
            "answer": answer,
            "sources": list(set(sources))
        }
    
    async def query_stream(self, question: str, chat_history: str = "") -> AsyncGenerator[Dict, None]:
        from app.core.llm import create_llm
        
        try:
            logger.info("Starting query stream for: %s", question[:100])
            
            docs: list[Document] = self.retriever.invoke(question)
            logger.info("Retrieved %d documents", len(docs))
            
            context = "\n\n".join([doc.page_content for doc in docs])

            history_section = ""
            if chat_history:
                history_section = f"Previous conversation:\n{chat_history}\n"

            prompt_text = self.prompt.format(
                context=context,
                question=question,
                chat_history=history_section
            )
            
            streaming_llm = create_llm(
                api_key=self.groq_api_key,
                model_name=self.model_name,
                temperature=0.7,
                streaming=True
            )
            
            full_response = ""
            async for chunk in streaming_llm.astream(prompt_text):
                if hasattr(chunk, 'content') and chunk.content:
                    token = clean_citations(chunk.content)
                    full_response += token
                    yield {
                        "type": "token",
                        "content": token
                    }
            
            logger.info("Streaming complete. Response length: %d chars", len(full_response))
            
            sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
            yield {
                "type": "sources",
                "sources": list(set(sources))
            }
            
            yield {
                "type": "done",
                "content": full_response
            }
            
        except Exception as e:
            logger.error("Error in query_stream: %s: %s", type(e).__name__, str(e), exc_info=True)
            yield {
                "type": "error",
                "content": f"{type(e).__name__}: {str(e)}"
            }