# 📚 B2B Support Copilot (RAG System with LangChain & ChromaDB)

Um sistema completo de **Retrieval-Augmented Generation (RAG)** construído para reduzir o volume de tickets de suporte nível 1 (N1) em operações logísticas de delivery. O chatbot consulta dinamicamente manuais internos e políticas da empresa antes de gerar uma resposta, garantindo precisão e evitando alucinações da IA.

## 🎯 Por que isso importa (Business Value)
Em plataformas de delivery, donos de restaurantes sobrecarregam o suporte com dúvidas que já estão documentadas nos manuais. LLMs puras (como o ChatGPT) não têm acesso aos processos internos de uma empresa. Ao implementar uma arquitetura RAG:
1. **Redução de Custos:** Automatiza a resolução de dúvidas processuais repetitivas (ex: "ciclo de repasse financeiro", "configuração de feriados").
2. **Zero Alucinações:** A IA é "ancorada" no texto do documento vetorial. Se a informação não estiver no manual, ela é programada para não inventar.
3. **Escalabilidade:** Para atualizar o conhecimento da IA, basta atualizar o `.md` e rodar a ingestão novamente, sem precisar fazer fine-tuning de modelos caros.

## 🏗️ Arquitetura e Stack Tecnológica
- **Orquestração de LLM:** LangChain (LCEL)
- **Banco de Dados Vetorial:** ChromaDB (Local/Embarcado)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Modelo de Inferência:** OpenAI `gpt-4o-mini`
- **Interface Gráfica:** Streamlit

## ⚙️ Como a Arquitetura Funciona
1. **Data Ingestion:** O script `ingest_data.py` lê documentos textuais, divide o texto em chunks (500 caracteres), converte esses textos em vetores matemáticos e os salva no ChromaDB.
2. **Retrieval (Busca):** Quando o usuário faz uma pergunta, o `rag_chain.py` converte a pergunta em vetor e busca os "pedaços" de texto matematicamente mais semelhantes no banco de dados.
3. **Generation:** A LLM recebe o prompt contendo a pergunta do usuário E o trecho do manual encontrado, gerando uma resposta contextualizada.

## 🚀 Como Executar Localmente

### 1. Preparação do Ambiente
Crie um ambiente virtual e instale as dependências:
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sua_api_key_aqui"
\`\`\`

### 2. Ingestão de Dados (Popular o Vector DB)
Execute o script de ingestão. Isso lerá o arquivo `data/manual_parceiro.md` e criará a pasta `db/` com os embeddings.
\`\`\`bash
python src/ingest_data.py
\`\`\`

### 3. Rodar a Interface Gráfica
Inicie o servidor Streamlit para interagir com o bot:
\`\`\`bash
streamlit run src/app.py
\`\`\`
O painel abrirá automaticamente em `http://localhost:8501`. Experimente perguntar: *"O que acontece se eu usar embalagem do concorrente?"*