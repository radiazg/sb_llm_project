import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
import os


FAISS_PATH = "faiss_data"
DIR_PATH_TXT = "data/txt"
DIR_PATH_CSV = 'data/csv/Key_Results_all.csv'

os.environ['GOOGLE_API_KEY'] = st.secrets["google_gemini"]["api_key_gemini"]


#get prompt RAG
def get_prompt():
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Eres un asistente, si recibes un input en Español, responde en Español. Si recibes un input en Ingles, responde en Ingles. No Incluya ningun AIMessage en el mensaje.
            Responde las siguientes preguntas en detalle usando el siguiente contexto e historia de chat:

            Contexto: {context}

            Historia de chat: {chat_history}
            """,
        ),
        ("human", "{input}"),
    ]
    )

    return prompt

def get_faiss():
    load_db = FAISS.load_local(FAISS_PATH, GoogleGenerativeAIEmbeddings(model="models/embedding-001"), allow_dangerous_deserialization=True)
    context = load_db.max_marginal_relevance_search(user_query, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in context])
    return context_text

def stream_response(response):
    for chunk in response:
        yield chunk.content
    
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
    #load_db = FAISS.load_local(FAISS_PATH, GoogleGenerativeAIEmbeddings(model="models/embedding-001"), allow_dangerous_deserialization=True)
    #context = load_db.max_marginal_relevance_search(user_query, k=3)
    #context_text = "\n\n---\n\n".join([doc.page_content for doc in context])

    
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    with st.chat_message("AI"):
        llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
        context_text = get_faiss()
        prompt = get_prompt()
        
        chain = prompt | llm
        ai_response = st.write_stream(stream_response(chain.stream(
            {
            "context": context_text,
            "chat_history": st.session_state.chat_history,
            "input": user_query,
            }
        )))
        #ai_response = st.write_stream(stream_response(get_response(user_query, st.session_state.chat_history, context_text)))
        
    st.session_state.chat_history.append(AIMessage(ai_response))
