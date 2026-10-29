import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Certifique-se de configurar o export OPENAI_API_KEY no terminal
api_key = os.getenv("OPENAI_API_KEY")

def process_and_ingest():
    print("1. Carregando o documento base...")
    loader = TextLoader("data/manual_parceiro.md", encoding="utf-8")
    document = loader.load()

    print("2. Fatiando o texto em pedaços (chunks)...")
    # Divide o texto para caber no limite de contexto da LLM
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(document)

    print("3. Gerando embeddings e salvando no ChromaDB...")
    # Converte o texto em vetores e salva na pasta ./db
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./db"
    )
    
    print("✅ Sucesso! Conhecimento ingerido no banco de dados vetorial.")

if __name__ == "__main__":
    process_and_ingest()