import streamlit as st
import time
import json
import os

#import judini
from judini.codegpt.codegpt import CodeGPT
from judini.codegpt.agent import Agent
from judini.codegpt.chat import Completion


from dotenv import load_dotenv
load_dotenv()

# CodeGPT Plus
api_key_env = os.getenv("CODEGPT_API_KEY")
agent_id_env = os.getenv("CODEGPT_AGENT_ID")

# layout
st.set_page_config(layout="centered")  
st.title("Welcome to Fantasy.AI")
st.write('A culture fantasy generator', unsafe_allow_html=True)
st.divider()

# sidebar
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("CodeGPT Plus API key", value=api_key_env, type="password")
agent_id = st.sidebar.text_input(f"Agent ID", value=agent_id_env)

idioma = st.sidebar.selectbox(
    'Language Base',
    ('English', 'German', 'Spanish'))
races = st.sidebar.multiselect(
    'What are you race base',
    ['Elf', 'Dwarfnome', 'Halfling'])

button = st.sidebar.button("Create", type="primary")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
def generate():
    if button:
        if len(races) > 0:
            # Add user message to chat history

            # Display user message in chat message container


            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                pre_prompt = '''
                Eres un experto en idiomas, linguista antigua y fantasía.

                Genera un idioma único, rico, quita letras y usa otros simbolos ascii de ser necesario.

                Si entran muchos razas como parametros debes generar siempre 1 solo tomando razas como influencia.
                '''
                prompt = {
                            "role": "user",
                            "content": pre_prompt + str(idioma) + "como base las usaran razas " + str(races) + " debes entregar el abcedario , como se pronuncia cada letra y combinaciones de cada letra en una tabla. Debes sumar en detalle reglas del idioma. Añade una leyenda corta sobre los que hablan el idioma y su origen."
                        }
                
                completion  =  Completion(api_key)
                response = completion.create(agent_id,prompt)


                raw_data = ''
                tokens = ''

                
                for line in response:
                    if line:
                        try:
                            full_response += str(line)
                            time.sleep(0.01)
                            # Add a blinking cursor to simulate typing
                            message_placeholder.markdown(full_response + "▌")
                        except json.JSONDecodeError:
                            print(f'Error : {line}')
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.warning("Please select at least one race before creating the language.")

generate()
