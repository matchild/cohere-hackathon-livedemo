## How do I set it up?
* Create a virtual environment: `conda create -n env00 python=3.10`
* Activate the created environment: `activate env00`
* Install the dependencies: `pip install -r requirements.txt`
* Copy the `.env-example` file into `.env` file and insert your secret keys [never push them on origin]

## How do I get it running?
* Create a folder "data": `mkdir data`
* Create a mock database: `python -m scripts.create_mock_db`
* Run the UI: `streamlit run main_ui.py`
