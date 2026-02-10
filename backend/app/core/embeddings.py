from langchain_community.embeddings import HuggingFaceEmbeddings


def create_embeddings():
   
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings':True}
    )
