"""Query engine for RAG system"""
from typing import Dict, AsyncGenerator
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from app.core.prompts import RAG_PROMPT_TEMPLATE


class QueryEngine:
    """Handles query processing and response generation"""
    
    def __init__(self, llm, vector_store, groq_api_key: str, model_name: str):
        """
        Initialize query engine
        
        Args:
            llm: Language model instance
            vector_store: Vector store instance
            groq_api_key: Groq API key for streaming
            model_name: Model name for streaming
        """
        self.llm = llm
        self.vector_store = vector_store
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        
        # Create prompt template
        self.prompt = PromptTemplate(
            template=RAG_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
    
    def query(self, question: str) -> Dict:
        """
        Query the RAG system (non-streaming)
        
        Args:
            question: User question
        
        Returns:
            Dict: Answer and sources
        """
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(k=4),
            chain_type_kwargs={"prompt": self.prompt},
            return_source_documents=True
        )
        
        result = chain({"query": question})
        
        sources = [doc.metadata.get('source', 'Unknown') 
                  for doc in result.get('source_documents', [])]
        
        return {
            "answer": result['result'],
            "sources": list(set(sources))  # Remove duplicates
        }
    
    async def query_stream(self, question: str) -> AsyncGenerator[Dict, None]:
        """
        Query the RAG system with streaming response
        
        Args:
            question: User question
        
        Yields:
            Dict: Streaming response chunks
        """
        from app.core.llm import create_llm
        
        try:
            print(f"Starting query stream for: {question}")
            
            # Get relevant documents
            docs = self.vector_store.get_relevant_documents(question, k=4)
            print(f"Retrieved {len(docs)} documents")
            
            # Build context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Format prompt
            prompt = self.prompt.format(context=context, question=question)
            
            # Create streaming LLM
            streaming_llm = create_llm(
                api_key=self.groq_api_key,
                model_name=self.model_name,
                temperature=0.7,
                streaming=True
            )
            
            print("Starting to stream response...")
            # Stream response
            full_response = ""
            async for chunk in streaming_llm.astream(prompt):
                if hasattr(chunk, 'content') and chunk.content:
                    token = chunk.content
                    full_response += token
                    yield {
                        "type": "token",
                        "content": token
                    }
            
            print(f"Streaming complete. Full response length: {len(full_response)}")
            
            # Send sources
            sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
            yield {
                "type": "sources",
                "content": sources
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
