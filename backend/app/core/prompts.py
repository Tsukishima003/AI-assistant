"""Prompt templates for RAG system"""

# RAG prompt template
RAG_PROMPT_TEMPLATE = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always cite the source documents when providing information from them.

Context:
{context}

Question: {question}

Helpful Answer:"""
