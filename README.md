# guarani-rag-2025

# Generación de Texto Sintético en Guaraní mediante Transformaciones Gramaticales  
**Comparativa: LLM Prompting (sin RAG) vs. Sistema RAG**  
Diplomado en NLP & IA – FPUNA 2025

## Integrantes
- Odilón Nolf Sánchez

## Objetivo del proyecto
Desarrollar y comparar dos agentes conversacionales capaces de generar texto sintético en guaraní aplicando transformaciones gramaticales específicas (tiempo verbal, persona, nasalización, posesivos, etc.):

1. Chatbot sin RAG → solo prompting con Gemma 3 27B + Llama 3.3 70B y Llama 3.3 70B Instruct
2. Chatbot con RAG → recuperación de fragmentos del Diccionario y Gramática Guaraní usando FAISS

## Estructura del repositorio
.
├── final_project_guide.ipynb      ← Entrega oficial (plantilla completada)
├── README.md                      ← estas instrucciones
├── requirements.txt
├── data/
│   ├── Diccionario_Guarani-Espanol.pdf
│   └── Gramatica_guarani.pdf
├── no_rag_chatbot/                ← agente solo prompting
│   ├── app.py
│   └── chainlit.md
└── rag_chatbot/                   ← agente con RAG + FAISS
├── app.py
└── chainlit.md


## Instalación rápida (una sola vez)

```bash
git clone https://github.com/onolf/guarani-rag-2025.git
cd guarani-rag-2025
pip install -r requirements.txt

# Chatbot sin RAG
chainlit run no_rag_chatbot/app.py -w
# Chatbot con RAG
chainlit run rag_chatbot/app.py -w

# URLs públicas (ejemplo con localtunnel – opcional)
# Terminal 1
lt --port 8000
# Terminal 2  
lt --port 8001

```
## Modelos utilizados (OpenRouter)
Ambos chatbots usan los siguientes modelos vía OpenRouter:

* google/gemma-2-27b-it + meta-llama/llama-3.3-70b-instruct
* meta-llama/llama-3.3-70b-instruct

Necesitás tu API key de OpenRouter en la variable de entorno OPENROUTER_API_KEY