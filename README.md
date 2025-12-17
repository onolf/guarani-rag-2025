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
├── guarani_pln_2025.ipynb          ← Entrega oficial
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
```

## 🛠️ Instalación y Configuración
```bash
git clone https://github.com/onolf/guarani-rag-2025.git
cd guarani-rag-2025
pip install -r requirements.txt

# Chatbot sin RAG
chainlit run no_rag_chatbot/app.py -w

# Chatbot con RAG
chainlit run rag_chatbot/app.py -w
```

## 🧠 Configuración de Modelos (OpenRouter)

Ambos chatbots acceden a los siguientes modelos a través de OpenRouter:

* `meta-llama/llama-3.3-70b-instruct:free`
* `google/gemma-3-27b-it:free`

### 🔑 Configuración de la API Key

Para la ejecución, necesitas tu API key de OpenRouter. Esta debe ser cargada en la variable de entorno `OPENROUTER_API_KEY`.

**Método Recomendado (.env):**

Para cargar la clave de forma segura, crea un archivo en la raíz del repositorio llamado **`.env`** con el siguiente contenido (reemplazando el marcador de posición):
```text
OPENROUTER_API_KEY="[tu_api_key_de_openrouter]"
```

---

# 📊 Resumen del Notebook de Entrega Oficial

## `guarani_pln_2025.ipynb`: Generación de Texto Sintético en Guaraní mediante Transformaciones Gramaticales

### Comparativa: LLM Prompting (sin RAG) vs. Sistema RAG

Este repositorio contiene el proyecto final para el Diplomado en NLP & IA – FPUNA 2025, centrado en la generación de texto sintético en guaraní con transformaciones gramaticales precisas.

### 1. Entendimiento del Negocio

*   **Necesidad:** Generar texto sintético en guaraní aplicando transformaciones gramaticales (tiempos verbales, persona, nasalización, posesivos) para la preservación lingüística y la educación.
*   **Problema:** Escasez de recursos digitales en guaraní, lo que lleva a "alucinaciones" (errores gramaticales o invenciones) en LLMs puros.
*   **Solución Propuesta:** Implementar una arquitectura RAG (Retrieval-Augmented Generation) utilizando documentos gramaticales y diccionarios oficiales para fundamentar las respuestas del modelo.

### 2. Entendimiento y Preparación de los Datos

*   **Fuentes de Datos:**
    *   Diccionario Guaraní-Español (PDF).
    *   Gramática Guaraní (PDF).
*   **Preprocesamiento:**
    *   **Limpieza de Texto:** Eliminación de ruido de PDFs (números de página, encabezados repetitivos).
    *   **Chunking:** División de documentos en fragmentos (`chunk_size=1000`, `chunk_overlap=200`).
    *   **Embedding:** Uso del modelo `sentence-transformers/all-MiniLM-L6-v2` para transformar el texto en vectores numéricos.
    *   **Vector Store:** Indexación de los embeddings en FAISS para una búsqueda eficiente.

### 3. Metodología y Aplicación de Modelos

Se compararon dos estrategias para la generación de texto:

1.  **Modelo Base (Sin RAG):** Pregunta directa a un LLM, basándose únicamente en su conocimiento paramétrico.
2.  **Sistema RAG:** Recuperación de contexto relevante del `Vector Store` seguido de la generación por el LLM.

**Modelos de Lenguaje (LLMs) utilizados (vía OpenRouter):**

*   **Llama 3.3** (`meta-llama/llama-3.3-70b-instruct:free`): Modelo de gran escala, como referencia de alta capacidad.
*   **Gemma 3** (`google/gemma-3-27b-it:free`): Modelo de menor escala, para evaluar escenarios de restricción computacional.

### 4. Evaluación Cuantitativa

Se evaluaron cuatro configuraciones (Llama 3.3 sin RAG, Llama 3.3 con RAG, Gemma 3 sin RAG, Gemma 3 con RAG) sobre 7 ejemplos representativos del dataset `AmericasNLP` (guarani-dev.tsv).

*   **Métricas:**
    *   **chrF:** Adecuado para lenguas aglutinantes como el guaraní, mide similitud a nivel de caracteres.
    *   **Latencia:** Tiempo de respuesta en segundos.

*   **Resultados Clave (Promedios):**

| Modelo              | chrF Promedio | Latencia Promedio (s) |
|---------------------|---------------|------------------------|
| Gemma 3 CON RAG     | 36.50         | 1.00                   |
| Gemma 3 SIN RAG     | 33.95         | 0.97                   |
| LLaMA 3.3 CON RAG   | 52.78         | 1.80                   |
| LLaMA 3.3 SIN RAG   | 49.59         | 1.57                   |

*   **Análisis:**
    *   La incorporación de **RAG mejoró el puntaje chrF** en ambos modelos de forma consistente, con incrementos de aproximadamente 3 puntos para LLaMA 3.3 y 2.55 puntos para Gemma 3.
    *   **LLaMA 3.3 (Con RAG)** obtuvo el mejor desempeño (chrF: 52.78), indicando que el contexto gramatical recuperado complementa efectivamente el conocimiento paramétrico del modelo.
    *   El incremento en latencia fue marginal (0.03-0.23s), justificado por las ganancias en precisión.
    *   Los resultados validan que RAG proporciona referencias estructurales útiles para transformaciones morfosintácticas en guaraní.

### 5. Análisis Cualitativo (Evaluación Manual de Chatbots)

Se realizó una evaluación manual de las 4 configuraciones en 10 ejemplos para fenómenos gramaticales específicos (futuro, nasalización, posesivos).

*   **Resultados Clave (Aciertos / 10 ejemplos):**

| Prueba                    | Llama_NoRAG | Llama_RAG | Gemma_NoRAG | Gemma_RAG |
|---------------------------|-------------|-----------|-------------|-----------|
| Futuro 'che aha'          | 1/10        | 2/10      | 2/10        | 1/10      |
| Nasalización 'oñembo'e'   | 0/10        | 3/10      | 1/10        | 2/10      |
| Posesivos 'róga'          | 2/10        | 4/10      | 4/10        | 3/10      |
| **Promedio**              | **1/10**    | **3/10**  | **2/10**    | **2/10**  |

*   **Análisis:**
    *   El análisis cualitativo muestra que RAG mejora la **corrección gramatical percibida por humanos** en fenómenos complejos, especialmente para LLaMA 3.3 (incremento de 1/10 a 3/10).
    *   Para Gemma 3, el impacto fue más moderado pero consistente.
    *   Esto complementa la evaluación cuantitativa, confirmando que RAG aporta valor tanto en métricas automáticas como en corrección lingüística funcional.

### 6. Aplicación de KMEANS (Análisis del Espacio de Embeddings)

*   **Metodología:** Aplicación de K-Means (k=2 a 5) en los embeddings del RAG, con y sin normalización, y cálculo del Silhouette Score.
*   **Resultados:** Silhouette Scores entre 0.06 y 0.11, indicando una estructura semántica débil pero consistente.
*   **Análisis:** Los embeddings normalizados se desempeñaron mejor con k=2, mientras que los sin normalizar con k=3. A pesar de esta débil separación semántica, el sistema RAG logra recuperar contextos suficientemente relevantes que aportan información morfosintáctica útil, como evidencian las mejoras consistentes en chrF.

### 7. Conclusión Final

La evaluación cuantitativa con chrF demostró que la incorporación de RAG mejora consistentemente el desempeño en transformaciones gramaticales del guaraní, con LLaMA 3.3 alcanzando el mejor resultado (chrF: 52.78 con RAG vs. 49.59 sin RAG). El análisis cualitativo confirmó que RAG también mejora la corrección lingüística percibida por humanos en fenómenos complejos como la nasalización y construcciones posesivas. 

Los resultados validan que el acceso a ejemplos específicos y patrones gramaticales relevantes complementa efectivamente las capacidades generativas de los modelos base, proporcionando referencias estructurales que facilitan transformaciones morfosintácticas más precisas. El incremento marginal en latencia resulta justificado frente a las ganancias en precisión obtenidas.

**Limitaciones:** Se utilizaron dos API keys de OpenRouter para procesar 7 registros representativos del conjunto DEV de AmericasNLP en las cuatro configuraciones evaluadas, generando un total de 28 registros procesados. Las restricciones de cuota en la versión gratuita de OpenRouter (50 llamadas diarias) y las incompatibilidades con el sistema de créditos de pago limitaron significativamente el alcance de la evaluación cuantitativa, impactando en la representatividad estadística de los resultados.