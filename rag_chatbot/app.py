# =====================================================
#  AVAÑE'Ẽ DEL TARAGÜÍ – Chatbot CON RAG
#  Generación de texto sintético en guaraní con recuperación de conocimiento
#  Fuentes: Diccionario Guaraní-Español + Gramática Guaraní
#  Modelos: Gemma-2-27B + Llama-3.3-70B vía OpenRouter
# =======================================================

import os
import chainlit as cl
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# -----------------------------------------------------
# Configuración
# -----------------------------------------------------
DATA_PATH = "data"  # carpeta con los PDFs
VECTORSTORE_PATH = "rag_chatbot/vectorstore"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("Falta la variable OPENROUTER_API_KEY")

# Modelo LLM
llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct:free",
    # model="google/gemma-3-27b-it:free",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.5,
    max_tokens=1024,
)

# Embeddings (rápidos y buenos para guaraní)
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

# -----------------------------------------------------
# Construcción o carga de la base vectorial
# -----------------------------------------------------
@cl.cache
def get_retriever():
    if os.path.exists(VECTORSTORE_PATH):
        print("Cargando vectorstore existente...")
        vectorstore = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        print("Creando vectorstore por primera vez...")
        loader = PyPDFDirectoryLoader(DATA_PATH)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(docs)
        print(f"Fragmentos creados: {len(chunks)}")

        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)
        print("Vectorstore guardado!")

    return vectorstore.as_retriever(search_kwargs={"k": 5})

# -----------------------------------------------------
# Prompt RAG optimizado para guaraní
# -----------------------------------------------------
template = """Sos un lingüista experto en guaraní paraguayo que utiliza fuentes confiables.

Usá SOLO la siguiente información recuperada del Diccionario y la Gramática Guaraní para responder:

{context}

Pregunta del usuario:
{question}

Instrucciones:
- Respondé siempre en guaraní correcto (ortografía normativa: ã, ẽ, ĩ, õ, ũ, ỹ, ʼ).
- Aplicá transformaciones gramaticales precisas.
- Si no encontrás la información exacta, decí: "Ndaikatúi areko pe información precisa, ndaipóri ejemplo clarísimo".
- Nunca inventes reglas gramaticales.
- Si podés, incluí 2–3 variantes para mostrar flexión.

¡Respuesta en guaraní!"""

prompt = PromptTemplate.from_template(template)

# -----------------------------------------------------
# Cadena RAG
# -----------------------------------------------------
retriever = None  # se inicializa en on_chat_start

rag_chain = None

@cl.on_chat_start
async def start():
    global retriever, rag_chain

    await cl.Message(
        content="""
# AVAÑE'Ẽ DEL TARAGÜÍ

¡Mba’éichapa! Ko’ápe chatbot **CON RAG** (Recuperación Aumentada).

Usa el **Diccionario Guaraní-Español** y la **Gramática Guaraní** como fuente de conocimiento.

Ejemplos que podés probar:

- ¿Cómo se dice “yo voy a comer” en guaraní?
- Transformá “oñembo’e” al futuro con nasalización oral
- Dame todas las formas de “ahecha” en presente, pasado y futuro
- ¿Cuál es la regla del prefijo je-?

¡Eipota pe transformación ha rohechauka!
        """
    ).send()

    # Cargar retriever y crear cadena
    retriever = get_retriever()
    rag_chain = (
        {"context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])),
         "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    await cl.Message(content="Base de conocimiento cargada. ¡Eñe’ê guaraníme!").send()

# -----------------------------------------------------
# Procesar mensajes
# -----------------------------------------------------
@cl.on_message
async def main(message: cl.Message):
    if rag_chain is None:
        await cl.Message(content="Por favor esperá un momento...").send()
        return

    msg = cl.Message(content="")
    await msg.send()

    try:
        response = await rag_chain.ainvoke(message.content)
        await msg.stream_token(response)
    except Exception as e:
        await msg.stream_token(f"¡Error!: {str(e)}")

    await msg.update()