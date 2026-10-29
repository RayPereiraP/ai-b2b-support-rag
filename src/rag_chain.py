from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def get_rag_chain():
    # 1. Conecta ao banco de dados existente
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(persist_directory="./db", embedding_function=embeddings)
    
    # Configura como um "retriever" (buscardor)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # 2. Template de Prompt com Contexto
    template = """Você é um assistente de suporte para parceiros de um app de delivery.
    Responda a pergunta do usuário baseando-se APENAS no contexto fornecido abaixo.
    Se a resposta não estiver no contexto, diga "Não encontrei essa informação no manual." não invente dados.

    Contexto da base de conhecimento:
    {context}

    Pergunta do Usuário: {question}
    
    Resposta:"""
    
    prompt = PromptTemplate.from_template(template)
    
    # 3. Define a LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 4. Cria a Chain (Corrente) usando LCEL (LangChain Expression Language)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain