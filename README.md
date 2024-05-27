# internal-chat-bot

## for the openai

- get open ai key
- create a file .env
- paste into the file: OPEN_AI_KEY = <your_open_ai_key>

## run the following for installation

- brew install pyenv-virtualenv
- for python version: pyenv install 3.11.3
- for creation of the env: pyenv virtualenv 3.11.3 internal-chat-bot

## for running the chatbot

- activate env: pyenv activate internal-chat-bot
- install requirements: pip install -r requirements.txt
- run the application: streamlit run app.py
