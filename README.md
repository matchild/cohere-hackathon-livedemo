# CoDA (Cohere Database Assistant)
⚡ The AI assistant for enterprise databases ⚡

## 🤔 What is it?
How many hours have you spent talking to experts within your company to understand where certain data is located and what it exactly means? Do not even mention if you are one of those experts!

CoDA engages in conversations with the experts in your company and retrieve all the hidden information about internal databases. All colleagues benefit by posing their questions directly to CoDA.

CoDa leverages [Cohere's API](https://docs.cohere.com/docs/the-cohere-platform) through its language model Command and its RAG capabilities.

## 🔧 How do I set it up?
* Create a virtual environment: `conda create -n env00 python=3.10`
* Activate the created environment: `activate env00`
* Install the dependencies: `pip install -r requirements.txt`
* Copy the `.env-example` file into `.env` file and insert your secret keys [never push them on origin]

## 🏃 How do I get it running?
* To have a version running fully locally, set `USE_LOCAL_VECTORSTORE = True` inside `app/constants.py`
* Run the UI: `streamlit run main_ui.py`
