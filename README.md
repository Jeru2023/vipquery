# streamlit-chat

This is a Streamlit chatbox demo working with chatGPT. But due to the restriction of text_area component, only pure text format supported in the chat box.

I'm going to implement another version in next project with cool features like voice chat, langchain integration with private API etc.

Note: sidebar and topbar reactions are not implemented yet.

![image](https://github.com/Jeru2023/streamlit-chat/blob/main/image/screen.jpg?raw=true)

## 🚀 Running locally
1. Install dependencies: `pip install -r requirements.txt`
1. Create secrets.toml as config file to store your OpenAI api key, keep this config file in .streamlit folder.
   1. Replace YOUR_KEY with your actual API key: `OPENAI_KEY="YOUR_KEY"`
1. To start the app: `streamlit run app.py`
