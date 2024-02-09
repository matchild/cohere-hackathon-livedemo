import streamlit as st

from app.agents.pull import PullAgent
from app.connectors.csv_connector import CSVConnector
from app.connectors.pdf_connector import PDFConnector


def chat_ui_pull() -> None:
    """Chatbot UI for pull chat"""

    _CONTAINER_HEIGHT = 400
    _NUMBER_OF_AI_QUESTIONS = 3

    state = st.session_state

    if "init_pull" not in state:
        state["init_pull"]: bool = True
        state["messages_pull"]: list[dict[str, str]] = []
        state["connector"]: CSVConnector | PDFConnector | None = None
        state["file_uploader_key"] = 0
        state["ai_questions_left"] = 0
        state["current_ai_question"]: str = None
        state["ai_questions_left"] = _NUMBER_OF_AI_QUESTIONS
        state["inputs"]: dict[str, list[str]] = {
            "inputs_required": [],
            "inputs_required_prompts": [],
        }
        state["outputs"]: list[dict[str, str]] = []
        state["output_db"]: list = []

    st.title("Pull Chat 📮")

    col1, col2 = st.columns(2)
    reformulate_with_ai_on = col1.toggle("Activate reformulate requests with AI")
    questions_with_ai = col2.toggle("Personalized questions with AI")

    uploaded_file = st.file_uploader(
        "Upload your file", type=["csv", "pdf"], key=state["file_uploader_key"]
    )
    if uploaded_file is not None and state["connector"] is None:
        if uploaded_file.type == "text/csv":
            state["connector"] = CSVConnector(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            state["connector"] = PDFConnector(uploaded_file)

        state["inputs"] = state["connector"].get_specifications()
        next_message = state["inputs"]["inputs_required_prompts"][0]
        state["messages_pull"].append({"role": "ai", "message": next_message})

    col1, col2 = st.columns(2)

    with col1:
        st.header("Chat")

        container1 = st.container(height=_CONTAINER_HEIGHT)

        for message in state["messages_pull"]:
            container1.chat_message(message["role"]).markdown(message["message"])

        user_query = st.chat_input("Give details...")
        if user_query:
            container1.chat_message("user").markdown(user_query)

            # file format questions space #
            if len(state["inputs"]["inputs_required_prompts"]) > 1:
                state["outputs"].append(
                    {state["inputs"]["inputs_required"][0]: user_query}
                )
                state["inputs"]["inputs_required"] = state["inputs"]["inputs_required"][
                    1:
                ]
                state["inputs"]["inputs_required_prompts"] = state["inputs"][
                    "inputs_required_prompts"
                ][1:]
                next_message = state["inputs"]["inputs_required_prompts"][0]
                state["messages_pull"] += [
                    {"role": "human", "message": user_query},
                    {
                        "role": "ai",
                        "message": (
                            PullAgent().run_rephrasing(
                                next_message, chat_history=state["messages_pull"]
                            )
                            if reformulate_with_ai_on
                            else next_message
                        ),
                    },
                ]

            # file content questions space #
            elif (
                questions_with_ai
                and state["ai_questions_left"] == _NUMBER_OF_AI_QUESTIONS
            ):
                state["outputs"].append(
                    {state["inputs"]["inputs_required"][0]: user_query}
                )
                state["current_ai_question"] = PullAgent().run_formulating(
                    chat_history=state["messages_pull"]
                )
                state["messages_pull"] += [
                    {"role": "human", "message": user_query},
                    {
                        "role": "ai",
                        "message": (state["current_ai_question"]),
                    },
                ]
                state["ai_questions_left"] -= 1
                print(state["ai_questions_left"])

            elif questions_with_ai and state["ai_questions_left"] > 0:
                state["outputs"].append({state["current_ai_question"]: user_query})
                state["current_ai_question"] = PullAgent().run_formulating(
                    chat_history=state["messages_pull"]
                )
                state["messages_pull"] += [
                    {"role": "human", "message": user_query},
                    {
                        "role": "ai",
                        "message": (state["current_ai_question"]),
                    },
                ]
                state["ai_questions_left"] -= 1

            elif state["connector"] is not None:
                state["messages_pull"].append(
                    {
                        "role": "ai",
                        "message": "All the useful information has been collected! Thanks for your help! "
                        "You can now close this window or upload another file",
                    }
                )
                state["outputs"].append({state["current_ai_question"]: user_query})
                state["connector"].save_data(state["outputs"])
                with st.session_state["conn"].session as db_session:
                    state["output_db"] = state["connector"].upload_data(db=db_session)

                state["connector"] = None
                st.session_state["file_uploader_key"] += 1

            else:
                state["messages_pull"].append(
                    {
                        "role": "ai",
                        "message": "Upload a file to start!",
                    }
                )
            st.rerun()

    with col2:
        st.header("Database")

        container2 = st.container(height=_CONTAINER_HEIGHT)

        for db_object in state["output_db"]:
            obj_container = container2.container(border=True)

            obj_container.write(f"Registered {type(db_object).__name__[:-4]} object:")
            obj_container.json(
                {
                    "id": db_object.id,
                    "name": db_object.name,
                    "description": db_object.description,
                    "registered_at": db_object.registered_at,
                }
            )
