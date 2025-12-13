# =====================================================
#  AVAÑE'Ẽ DEL TARAGÜÍ – Chatbot SIN RAG
#  Generación de texto sintético en guaraní mediante prompting
#  Modelos: Gemma-2-27B + Llama-3.3-70B vía OpenRouter
# =====================================================

import os
import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# -----------------------------------------------------
# Configuración del modelo vía OpenRouter
# -----------------------------------------------------
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("Por favor define la variable de entorno OPENROUTER_API_KEY")

# Usaremos Llama-3.3-70B-Instruct como modelo principal
llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct:free",
    openai_api_key=openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=1024,
)

# -----------------------------------------------------
# Prompt optimizado para transformaciones gramaticales en guaraní
# -----------------------------------------------------
prompt_template = """
Sos un experto lingüista del idioma guaraní paraguayo. Tu tarea es generar texto sintético en guaraní aplicando transformaciones gramaticales precisas.

Instrucciones estrictas:
- Usa siempre ortografía normativa paraguaya (con tilde en nasales: ã, ẽ, ĩ, õ, ũ, ỹ y el signo ʼ para la saltillo).
- Respeta la gramática aglutinante del guaraní.
- Nunca mezcles español dentro de la respuesta en guaraní (solo si el usuario lo pide explícitamente).

Transformación solicitada por el usuario:
{message}

Responde únicamente en guaraní (salvo que te pidan traducción explícita).
Si necesitas ejemplos, podés incluir 2–3 variantes para mostrar flexión.

¡Mba’éichapa!
"""

prompt = PromptTemplate.from_template(prompt_template)

# -----------------------------------------------------
# Cadena LangChain
# -----------------------------------------------------
chain = (
    {"message": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# -----------------------------------------------------
# Interfaz Chainlit
# -----------------------------------------------------
@cl.on_chat_start
async def start():
    # Mensaje de bienvenida
    await cl.Message(
        content="""
# AVAÑE'Ẽ DEL TARAGÜÍ

¡Mba'éichapa! Ko'ápe roime generador de texto sintético en guaraní **sin RAG** (solo prompting).

Podés pedirme cosas como:

- Cambiame "che aha" al futuro → ?
- Poné "ndokatui" en tercera persona inclusiva
- Transformá "oñembo'e" al pasado con nasalización oral
- Hacé 5 variantes de "ahecha" en todos los tiempos

¡Eipota pe transformación ha rohechauka!
        """
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Mostrar indicador de escritura
    msg = cl.Message(content="")
    await msg.send()

    try:
        response = await chain.ainvoke(message.content)
        await msg.stream_token(response)
    except Exception as e:
        await msg.stream_token(f"¡Ay, ndaikatúi! Oiko jejavy: {str(e)}")
    
    await msg.update()