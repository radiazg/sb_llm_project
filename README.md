# sb_llm_project
Second brain LLM´s Project

## Objetivo del proyecto 

El objetivo del proyecto es crear un asistente usando Langchain como framework que permita tener un asistente de dialogo, un asistente de recuperación (RAG) y un asistente de  personal usando streamlit para como UI de chat.

## Información sobre los datos utilizados para el RAG.

Los archivos se almacenan en la carpeta data
```
 ├── data
       ├── csv      <- Datos scv
       ├── pdf      <- Datos pdf
       ├── txt      <- txt
```

## Información sobre ramas.

Este proyecto consta de dos ramas `main`y `agents`

La rama `main` tiene el asistente de chat y recuperación (RAG) usando el framework Langchain para crear cadenas; usa Google Generative AI como llm, por lo que debe la generar una API Key en Google AI Studio usando la free tier.

La rama `agents` tiene el asistente de chat, el asistente recuperación (RAG) y el sistente personal usando el framework Langchain para crear agentes con `Tools` que permite usarlas para responder a las preguntas hechas por el usuario. usa OpenAI (GPT-4o mini) como llm, por lo que debe la generar una API Key en OpenAI API y tener crédito para su uso.
```
├── tools
    ├── FAISS_search      <- Agente que recupera datos del indice FAISS generado
    ├── CSV_Agent         <- Agente que recupera datos del CSV con key results personales
```
## Instalar librerías requeridas para el proyecto

Antes de instalar las librerías, debe generar un entorno virtual de python como buena práctica.  A continuación en nuestro terminal ejecutamos:

```
python3 -m venv venv
```

Inicializar el entrono virtual

```
source venv/bin/activate
```

Luego instalar las librerías

`main`
```
pip install -r requirements2.txt
```
El archivo `requirements.txt` en la rama `main` es usado para depsplegar la app en Streamlit Cloud.


`agents`
```
pip install -r requirements.txt
```


## API KEY (Google GenerativeAI & OpenAI)

La API KEY de Google GenerativeAI se guarda en el archivo `secrets.toml` en la carpeta `.streamlit/`.

```
# .streamlit/secrets.toml

[google_gemini]
api_key_gemini = "your_key"
```

La API KEY de OpenAI se guarda en el archivo `secrets.toml` en la carpeta `.streamlit/`.

```
# .streamlit/secrets.toml

[openai]
api_key_openai = "your_key"
```

La carpeta `.streamlit` no se sincroniza con Github, por lo que debe crear esta carpeta y crear el archivo `secrets.toml`.

## Generar indices FAISS

Una vez instalado las librerías necesarias y para generar los datos en la base de datos vectorial debe ejecutar el Jupyter Notebook `load_data.ipynb`.

Este notebook genera los indices de la DB FAISS en la carpeta `faiss_data`.

## Lanzar la web app de Streamlit

En el terminal debemos ejecutar

```
streamlit run app.py
```

--------