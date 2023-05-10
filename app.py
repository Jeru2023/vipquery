import openai
import toml
import streamlit as st
import embeddings.query as qa_chain
import os
from utils.folder_updater import folder_updater

st.set_page_config(page_title='ChatGPT Assistant', layout='wide', page_icon='🍋')

#################################################################
##### Loading config
#################################################################
#os.environ["http_proxy"]="http://127.0.0.1:7890"
#os.environ["https_proxy"]="http://127.0.0.1:7890"

#################################################################
##### Generate response function
#################################################################
def generate_response(question, persist_directory):
	chain = qa_chain.get_chain(persist_directory)
	response = qa_chain.query(chain, question)
	return response

#################################################################
##### Building sidebar
#################################################################
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'''<h1 style=" padding :0">My Datasets</h1>''', unsafe_allow_html=True)
    with col2:
        mybtn = st.button("Create dataset folder")
        st.session_state.mybtn = mybtn
    if st.session_state.mybtn:
        col11, col22 = st.columns(2)
        with col11:
            st.text_input(
                "",
                label_visibility="collapsed", # placeholder="pls input your folder"
            )
        with col22:
            st.button("Save")
    with st.expander("Select my dataset folder"):
        st.write("folder1")
        st.write("folder2")
        st.write("folder3")

    st.markdown("# Control Panel 📌")
    context_level = st.slider('Context Level 👇', 1, 10, 4, 1)
    temperature = st.slider('Temperature 👇', 0.0, 2.0, 1.0, 0.5)
    top_p = st.slider('Top P 👇', 0.1, 1.0, 1.0, 0.1)
    presence_penalty = st.slider('Presence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
    frequency_penalty = st.slider('Frequence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
	#https://platform.openai.com/docs/api-reference/completions/create
    
    uploaded_files = st.file_uploader("Choose txt files", accept_multiple_files=True)
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

fu = folder_updater()
keys_list = fu.get_key_list()


st.session_state.options = st.multiselect(
    '请选择你要对话的数据集:(未来可多选，暂时请单选)',
    keys_list,

    )
options = st.session_state.options

if (len(options)>0):    
    print('dic is: ', str(fu.get_dict()))
    folder = fu.query_uuid(options[0])
    print('folder is: ', folder)
    persist_directory = f"db/{folder}"

prompt = st.text_input("输入问题后回车", placeholder="Enter your message here...")


if prompt:
	with st.spinner("Generating response..."):
		message_log.append({"role": "user", "content": prompt})
		#output = generate_response(message_log)
		print("persist_directory: ", persist_directory)
		output = generate_response(prompt, persist_directory)
		message_log.append({"role": "assistant", "content": output})
    	#store the output
		st.session_state['past'].append(prompt)
		st.session_state['generated'].append(output)

if st.session_state['generated']:
	for i in range(len(st.session_state['generated'])-1, -1, -1):
		st.markdown(f'''<div style='background:white;color:black;padding:10px'><b>**AI:**</b> {st.session_state["generated"][i]}</div>''',unsafe_allow_html=True)
		st.markdown(f'''<div style='background:#ddd;color:black;padding:10px'><b>**You:**</b> {st.session_state["past"][i]}</div>''',unsafe_allow_html=True)