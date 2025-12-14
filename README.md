# 🇵🇾 guarani-rag-2025

# 📝 Generación de Texto Sintético en Guaraní mediante Transformaciones Gramaticales

**Comparativa: LLM Prompting (sin RAG) vs. Sistema RAG**
Diplomado en NLP & IA – FPUNA 2025

## 🧑‍💻 Integrante
- Odilón Nolf Sánchez

## 🎯 Objetivo del Proyecto

Desarrollar y comparar dos agentes conversacionales capaces de generar texto sintético en guaraní aplicando transformaciones gramaticales específicas (tiempo verbal, persona, nasalización, posesivos, etc.):

1. **Chatbot sin RAG**: Implementación basada únicamente en *prompting* utilizando los modelos `google/gemma-3-27b` y `meta-llama/llama-3.3-70b-instruct`.
2. **Chatbot con RAG**: Implementación que utiliza la **Recuperación Aumentada por Generación (RAG)**, recuperando fragmentos del Diccionario y Gramática Guaraní mediante **FAISS**.

## 📂 Estructura del Repositorio

```text
.
├── final_project_guide.ipynb       ← Entrega oficial (plantilla completada)
├── README.md                       ← Archivo de instrucciones
├── requirements.txt
├── data/
│   ├── Diccionario_Guarani-Espanol.pdf
│   └── Gramatica_guarani.pdf
├── no_rag_chatbot/                 ← Agente solo prompting
│   ├── app.py
│   └── chainlit.md
└── rag_chatbot/                    ← Agente con RAG + FAISS
    ├── app.py
    └── chainlit.md


## 🛠️ Instalación y Configuración

```bash
git clone https://github.com/onolf/guarani-rag-2025.git
cd guarani-rag-2025
pip install -r requirements.txt

# Chatbot sin RAG
chainlit run no_rag_chatbot/app.py -w
# Chatbot con RAG
chainlit run rag_chatbot/app.py -w

### 🧠 Configuración de Modelos (OpenRouter)

Ambos chatbots acceden a los siguientes modelos a través de OpenRouter:

* `meta-llama/llama-3.3-70b-instruct:free`
* `google/gemma-3-27b-it:free`

#### 🔑 Configuración de la API Key

Para la ejecución, necesitas tu API key de OpenRouter. Esta debe ser cargada en la variable de entorno `OPENROUTER_API_KEY`.

**Método Recomendado (.env):**

Para cargar la clave de forma segura, crea un archivo en la raíz del repositorio llamado **`.env`** con el siguiente contenido (reemplazando el marcador de posición):

```text
OPENROUTER_API_KEY="[tu_api_key_de_openrouter]"