import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import AgentExecutor, Tool, initialize_agent
from langchain_experimental.agents import create_csv_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.llms import OpenAI
import os


FAISS_PATH = "faiss_data"
DIR_PATH_TXT = "data/txt"
DIR_PATH_CSV = 'data/csv/Key_Results_all.csv'

os.environ['GOOGLE_API_KEY'] = st.secrets["google_gemini"]["api_key_gemini"]
os.environ['OPENAI_API_KEY'] = st.secrets["openai"]["api_key_openai"]



#get prompt RAG
def get_prompt():
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Eres un asistente, si recibes un input en Español, responde en Español. Si recibes un input en Ingles, responde en Ingles. No Incluya ningun AIMessage en el mensaje.
            Al finalizar la respuesta final debes traducirla al Español.
            Responde las siguientes preguntas en detalle usando el siguiente contexto e historia de chat:

            Contexto: {context}

            Historia de chat: {chat_history}
            """,
        ),
        ("human", "{input}"),
    ]
    )

    return prompt

def get_faiss(user_query):
    load_db = FAISS.load_local(FAISS_PATH, GoogleGenerativeAIEmbeddings(model="models/embedding-001"), allow_dangerous_deserialization=True)
    context = load_db.max_marginal_relevance_search(user_query, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in context])
    return context_text

def stream_response(response):
    for chunk in response:
        yield chunk.content
    

tools = [
    Tool(
        name="FAISS_Search",
        func=get_faiss,
        description="Útil para cuando necesitas buscar información en tus documentos.",
    ),
    Tool(
        name = "CSV_Agent",
        func=create_csv_agent(OpenAI(temperature=0), DIR_PATH_CSV, verbose=True, allow_dangerous_code=True),
        description="Útil para cuando necesitas consultar el archivo CSV 'Key_Results_all.csv'.",
    )
]


# rev chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    

#stremlit head
st.set_page_config(page_title="Second Brain GPT", page_icon="💡")
col1, mid, col2 = st.columns([1,2,20])
with col1:
    st.image("second_brain_icon.jpg", output_format="JPEG", width=100)
with col2:
    st.title("Second Brain GPT")
    st.write("Second Brain GPT es un asistente")

#streamlit conversation 
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

#user input
user_query = st.chat_input("Tu pregunta")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    with st.chat_message("AI"):
        prompt = get_prompt()
        llm = ChatOpenAI(model_name="gpt-4o-mini", streaming=True)
        context_text = get_faiss(user_query)
        #chain = prompt | llm
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
        
        #ai_response = chain.stream(
        ai_response = agent.invoke(
            {
                "context" : context_text,
                "chat_history" : st.session_state.chat_history,
                "input": user_query
            }
        )
        st.write(ai_response["output"])
        #st.write_stream(stream_response(ai_response))
        
    st.session_state.chat_history.append(AIMessage(ai_response["output"]))
    #st.session_state.chat_history.append(AIMessage(ai_response))