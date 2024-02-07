import streamlit as st

from app.connectors.csv_connector import CSVConnector
from app.connectors.pdf_connector import PDFConnector

# TODO: handle when all information are collected (save output to db, print success message and reset connector)


def chat_ui_pull() -> None:
    """Chatbot UI for pull chat"""

    _CONTAINER_HEIGHT = 400
    state = st.session_state

    if "init_pull" not in state:
        state["init_pull"]: bool = True
        state["messages_pull"]: list[dict[str, str]] = []
        state["connector"]: CSVConnector | PDFConnector | None = None
        state["inputs"]: dict[str, list[str]] = {
            "inputs_required": [],
            "inputs_required_prompts": [],
        }
        state["outputs"]: list[dict[str, str]] = []

    st.title("Pull Chatbot 🤖")

    uploaded_file = st.file_uploader("Upload your file", type=["csv", "pdf"])
    if uploaded_file is not None and state["connector"] is None:
        if uploaded_file.type == "text/csv":
            state["connector"] = CSVConnector(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            state["connector"] = PDFConnector(uploaded_file)

        state["inputs"] = state["connector"].get_specifications()
        state["messages_pull"].append(
            {
                "role": "ai",
                "message": state["inputs"]["inputs_required_prompts"][0],
            }
        )

    col1, col2 = st.columns(2)

    with col1:
        st.header("Chat")

        container1 = st.container(height=_CONTAINER_HEIGHT)

        for message in state["messages_pull"]:
            container1.chat_message(message["role"]).markdown(message["message"])

        user_query = st.chat_input("Ask something...")
        if user_query:
            container1.chat_message("user").markdown(user_query)

            state["outputs"].append({state["inputs"]["inputs_required"][0]: user_query})
            state["inputs"]["inputs_required"] = state["inputs"]["inputs_required"][1:]
            state["inputs"]["inputs_required_prompts"] = state["inputs"][
                "inputs_required_prompts"
            ][1:]

            state["messages_pull"] += [
                {"role": "human", "message": user_query},
                {
                    "role": "ai",
                    "message": state["inputs"]["inputs_required_prompts"][0],
                },
            ]
            st.rerun()

    with col2:
        st.header("Database")

        container2 = st.container(height=_CONTAINER_HEIGHT)
        container2.json(state["outputs"])

        # with state["conn"].session as db_session:
        # db_object = get_dataframe_by_id(db=db_session, id=1)

        # obj_container = container2.container(border=True)
        # obj_container.write("Registered object:")
        # obj_container.json(
        #     {
        #         "id": db_object.id,
        #         "name": db_object.name,
        #         "description": db_object.description,
        #         "registered_at": db_object.registered_at,
        #     }
        # )
