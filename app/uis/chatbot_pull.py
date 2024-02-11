import time

import streamlit as st

from app.agents.pull import PullAgent
from app.connectors.csv_connector import CSVConnector
from app.connectors.pdf_connector import PDFConnector
from app.uis.utils import st_chat_containers


def chat_ui_pull() -> None:
    """Chatbot UI for pull chat"""

    _NUMBER_OF_AI_QUESTIONS = 2
    _REFORMULATE_AI = True
    _QUESTIONS_AI = True

    state = st.session_state

    if "init_pull" not in state or not state["init_pull"]:
        st.warning(
            "Uploading documents to this chat won't store any data into the memory. "
            "To try Data Submission and Retrieval in a more complete way, "
            "run the repo locally  ",
            icon="⚠️",
        )
        state["init_pull"]: bool = True
        state["summary_chat"] = "Answer to more questions to generate the insights..."
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
        state["outputs"]: dict[str, dict[str, str]] = {}
        state["outputs"]["required"] = {}
        state["outputs"]["additional"] = {}
        state["output_db"]: list = {}

    st.title("Submission Chat 📮")

    reformulate_with_ai_on = _REFORMULATE_AI
    questions_with_ai = _QUESTIONS_AI

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

    container1, container2, user_query = st_chat_containers(
        "Chat", "Information submitted"
    )

    with container1:
        for message in state["messages_pull"]:
            st.chat_message(message["role"]).markdown(message["message"])

        if user_query and state["connector"] is not None:
            st.chat_message("user").markdown(user_query)

            if not PullAgent().is_run_classifying_ok(user_query):
                state["messages_pull"].pop(-1)
                with st.spinner("Reformulating..."):
                    state["messages_pull"].append(
                        {
                            "role": "ai",
                            "message": (
                                PullAgent().run_rephrasing(
                                    state["inputs"]["inputs_required_prompts"][0],
                                    chat_history=state["messages_pull"],
                                )
                                if reformulate_with_ai_on
                                else state["inputs"]["inputs_required_prompts"][0]
                            ),
                        }
                    )
                st.rerun()

            # file format questions space #
            elif len(state["inputs"]["inputs_required_prompts"]) > 1:
                state["outputs"]["required"][
                    state["inputs"]["inputs_required"][0]
                ] = user_query
                state["inputs"]["inputs_required"] = state["inputs"]["inputs_required"][
                    1:
                ]
                state["inputs"]["inputs_required_prompts"] = state["inputs"][
                    "inputs_required_prompts"
                ][1:]
                next_message = state["inputs"]["inputs_required_prompts"][0]
                with st.spinner("Generating next question..."):
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
                state["outputs"]["required"][
                    state["inputs"]["inputs_required"][0]
                ] = user_query
                state["current_ai_question"] = PullAgent().run_formulating(
                    chat_history=state["messages_pull"]
                )
                with st.spinner("Generating next question..."):
                    state["messages_pull"] += [
                        {"role": "human", "message": user_query},
                        {
                            "role": "ai",
                            "message": (state["current_ai_question"]),
                        },
                    ]
                state["ai_questions_left"] -= 1

            elif questions_with_ai and state["ai_questions_left"] > 0:
                state["outputs"]["additional"][
                    state["current_ai_question"]
                ] = user_query
                with st.spinner("Generating next question..."):
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
                state["outputs"]["additional"][
                    state["current_ai_question"]
                ] = user_query
                print(state["outputs"])
                state["connector"].save_data(state["outputs"])
                with st.session_state["conn"].session as db_session:
                    with st.spinner("Saving data and answers..."):
                        state["output_db"] = state["connector"].upload_data(
                            db=db_session
                        )

                state["connector"] = None
                st.session_state["file_uploader_key"] += 1

                with st.spinner(
                    "All the useful information has been collected! I'll refresh the chat in a bit..."
                ):
                    time.sleep(3)
                    state["init_pull"] = False

            with st.spinner("Generating insights..."):
                result_summary = PullAgent().summarize_chat(state["messages_pull"])
                if len(result_summary) > 0:
                    state["summary_chat"] = result_summary
            st.rerun()

    with container2:
        st.markdown(state["summary_chat"])

        # for db_object in state["output_db"]:
        #     obj_container = container2.container(border=True)
        #
        #     obj_container.write(f"Registered {type(db_object).__name__[:-4]} object:")
        #     obj_container.json(
        #         {
        #             "id": db_object.id,
        #             "name": db_object.name,
        #             "description": db_object.description,
        #             "registered_at": db_object.registered_at,
        #         }
        #     )
