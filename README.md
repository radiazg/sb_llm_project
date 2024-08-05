# sb_llm_project
Second brain LLM´s Project

secop_project
==============================


## Objetivo del proyecto 

El objetivo del proyecto es grar un agente de LLM con diferentes tools para tener un agente de dialogo, un agente de respuesta con RAG y un agente personal.
Se usa Google Gemini como LLM.


## Información sobre los datos utilizados para el RAG.

Los archivos se almacenan en la carpeta data

### Instalar librerías requeridas para el proyecto

Antes de instalar las librerías, debe generar un entorno virtual de python como buena práctica.  A continuación en nuestro terminal ejecutamos:

```
python3 -m venv venv
```

Inicializar el entrono virtual

```
source venv/bin/activate
```

Luego instalar las librerías

```
pip install -r requirements.txt
```

## Generar Modelo

Una vez instalado las librerías necesarias y para generar los datos en la base de datos vectorial debe ejecutar el Jupyter Notebook `load_data.ipynb`.

Este notebook genera los indices de la DB FAISS en la carpeta `faiss_data`.

## Lanzar la web app de Streamlit

En el terminal debemos ejecutar

```
streamlit run app.py
```

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>