import openai
import toml
import streamlit as st
import embeddings.query as qa_chain
import os

from embeddings.ingest import ingest
from utils.folder_updater import folder_updater

st.set_page_config(page_title='ChatGPT Assistant', layout='wide', page_icon='🍋')


#################################################################
##### Loading config
#################################################################

os.environ["http_proxy"]="http://127.0.0.1:7890"
os.environ["https_proxy"]="http://127.0.0.1:7890"

#################################################################
##### Generate response function
#################################################################

def get_persiste_directory(option):
    folder = fu.query_uuid(option)
    print('folder is: ', folder)
    return f"db/{folder}"

def generate_summary(question, options, **chain_kwargs):
    response = ''
    for option in options:
        print(f'option is {option}')
        persist_directory = get_persiste_directory(option)
        response += f'<br><b>以下容根据{option}中内容回答</b><br><br>'
        response += generate_response(question, persist_directory, **chain_kwargs) + '<br>'

    return response

def generate_response(question, persist_directory, **chain_kwargs):
    response = qa_chain.query(question, persist_directory, **chain_kwargs)
    return response

def query_change():
    st.session_state.on_change = True


fu = folder_updater()
keys_list = [i for i in fu.get_key_list()]

if not st.session_state.get("new_folder"):
    st.session_state.new_folder = ""
if not st.session_state.get("expanded"):
    st.session_state.expanded = False

if not st.session_state.get("file_change"):
    st.session_state.file_change = []
if not st.session_state.get('on_change'):
    st.session_state.on_change = False

#################################################################
##### Building sidebar
#################################################################

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'''<h1 style=" padding :0">My Datasets</h1>''', unsafe_allow_html=True)
    with col2:
        mybtn = st.button("Create Folder")
        st.session_state.mybtn = mybtn
    if st.session_state.mybtn:
        st.text_input(
            "add folder",
            label_visibility="collapsed",
            key="new_folder"
        )
    # 有无新目录 且 新目录未被创建
    if st.session_state.new_folder and st.session_state.new_folder not in keys_list:
        keys_list.append(st.session_state.new_folder)
        fu.create_folder(st.session_state.new_folder)
        st.session_state.new_folder = ""
        st.session_state.expanded = True

    with st.expander("See My Folder", expanded=st.session_state.expanded):
        st.radio(
            "folder radio",
            keys_list,
            label_visibility="collapsed",
            key="choice_folder"
        )

    # st.markdown("# Control Panel 📌")
    # context_level = st.slider('Context Level 👇', 1, 10, 4, 1)
    # temperature = st.slider('Temperature 👇', 0.0, 2.0, 1.0, 0.5)
    # top_p = st.slider('Top P 👇', 0.1, 1.0, 1.0, 0.1)
    # presence_penalty = st.slider('Presence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
    # frequency_penalty = st.slider('Frequence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
    # https://platform.openai.com/docs/api-reference/completions/create
    # if st.session_state.get('uploaded_files'):
    #     # print(st.session_state.get('uploaded_files'))
    #     # st.session_state['uploaded_files'] = []
    #     del st.session_state['uploaded_files']
    # if st.session_state['uploaded_files'].__len__() > 0:
    #     del st.session_state['uploaded_files']

    st.file_uploader(
        f"当前上传目录为:  {st.session_state.choice_folder}",
        accept_multiple_files=True,
        key='uploaded_files'
    )
        
    if st.session_state.get('uploaded_files'):
        for uploaded_file in st.session_state['uploaded_files']:
            bytes_data = uploaded_file.read()
            fu.save_files(st.session_state.choice_folder, uploaded_file.name, bytes_data)
            
        if len(st.session_state['uploaded_files']) > 0 and st.session_state.file_change != st.session_state[
            'uploaded_files']:
            print(st.session_state.choice_folder)
            ingest(st.session_state.choice_folder)
            print("ingest success")
            st.session_state.file_change = st.session_state['uploaded_files']
            del st.session_state['uploaded_files']

#################################################################
##### Chatbox
#################################################################	

if 'past' not in st.session_state:
    st.session_state['past'] = []

if "generated" not in st.session_state:
    st.session_state["generated"] = []

message_log = [{"role": "user", "content": "hi"}]

st.header("Welcome to Jeru's CHATBOT 🍋")



col1, col2 = st.columns(2)
options = col1.multiselect(
    '请选择你要对话的数据集:(可多选)',
    keys_list,

)

verbose = col2.checkbox(label="Enable Chain of Thought", value=True)

st.text_input(
    "输入问题后回车",
    placeholder="Enter your message here...",
    key="query",
    on_change=query_change
)
if st.session_state.query and len(options) > 0 and st.session_state.on_change:
    with st.spinner("Generating response..."):
        chain_kwargs = {'verbose': verbose}

        message_log.append({"role": "user", "content": st.session_state.query})
        # output = generate_response(message_log)
        output = generate_summary(st.session_state.query, options, **chain_kwargs)

        message_log.append({"role": "assistant", "content": output})
        # store the output
        st.session_state['past'].append(st.session_state.query)
        st.session_state['generated'].append(output)
        # del st.session_state.query


if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        st.markdown(
            f'''<div style='background:#ddd;color:black;padding:10px'><b>**You:**</b> {st.session_state["past"][i]}</div>''',
            unsafe_allow_html=True)
        st.markdown(
            f'''<div style='background:white;color:black;padding:10px'><b>**AI:**</b> {st.session_state["generated"][i]}</div><br>''',
            unsafe_allow_html=True)

st.session_state.on_change = False