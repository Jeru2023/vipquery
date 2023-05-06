import openai
import toml
import streamlit as st
from streamlit_option_menu import option_menu
import embeddings.query as qa_chain
import os
import tkinter as tk
from tkinter import filedialog

st.set_page_config(page_title='ChatGPT Assistant', layout='wide', page_icon='🍋')

#################################################################
##### Loading config
#################################################################
persist_directory = "db"
source_directory = "docs"

os.environ["http_proxy"]="http://127.0.0.1:7890"
os.environ["https_proxy"]="http://127.0.0.1:7890"

#################################################################
##### Generate response function
#################################################################
def generate_response_backup(message_log):
    """
    Use OpenAI's ChatCompletion API to get the chatbot's response.
    """
    # Set the model name and creativity level
    model_name = "gpt-3.5-turbo"
    temperature = 0.7

    # Call the ChatCompletion API
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=message_log,
        temperature=temperature,
    )

    # Find the first text response from the chatbot
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no text response is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def generate_response(question):
	chain = qa_chain.get_chain(persist_directory)
	response = qa_chain.query(chain, question)
	return response

#################################################################
##### Building topbar
#################################################################
topbar = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
	icons=['house', 'cloud-upload', "list-task", 'gear'], 
	menu_icon="cast", default_index=0, orientation="horizontal",
	styles={
		"nav-link": {"--hover-color": "#eee"},		
	}
)	

#################################################################
##### Building sidebar
#################################################################
with st.sidebar:

    filelist=[]
    for root, dirs, files in os.walk("embeddings"):
        for file in files:
             filename=os.path.join(root, file)
             filelist.append(filename)
        st.write(filelist)

    # Set up tkinter
    root = tk.Tk()
    root.withdraw()

    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    # Folder picker button
    st.title('Folder Picker')
    st.write('Please select a folder:')
    clicked = st.button('Folder Picker')
    if clicked:
        dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
    
    st.header("Control Panel")
    st.markdown("# Control Panel 📌")
    context_level = st.slider('Context Level 👇', 1, 10, 4, 1)
    temperature = st.slider('Temperature 👇', 0.0, 2.0, 1.0, 0.5)
    top_p = st.slider('Top P 👇', 0.1, 1.0, 1.0, 0.1)
    presence_penalty = st.slider('Presence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
    frequency_penalty = st.slider('Frequence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
	#https://platform.openai.com/docs/api-reference/completions/create
    
    uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

#################################################################
##### Chatbox
#################################################################	
if 'past' not in st.session_state:
	st.session_state['past'] = []

if "generated" not in st.session_state:
    st.session_state["generated"] = []
	
message_log = [{"role": "user", "content": "hi"}]
	
st.header("Welcome to Jeru's CHATBOT 🍋")

prompt = st.text_input("Prompt", placeholder="Enter your message here...")

#st.text(print('hello'))
#st.text(test_query())

if st.button("Send"):
	with st.spinner("Generating response..."):
		message_log.append({"role": "user", "content": prompt})
		#output = generate_response(message_log)
		output = generate_response(prompt)
		message_log.append({"role": "assistant", "content": output})
    	#store the output
		st.session_state['past'].append(prompt)
		st.session_state['generated'].append(output)

if st.session_state['generated']:
	for i in range(len(st.session_state['generated'])-1, -1, -1):
		st.markdown(f'''<div style='background:white;color:black;padding:10px'><b>**AI:**</b> {st.session_state["generated"][i]}</div>''',unsafe_allow_html=True)
		st.markdown(f'''<div style='background:#ddd;color:black;padding:10px'><b>**You:**</b> {st.session_state["past"][i]}</div>''',unsafe_allow_html=True)