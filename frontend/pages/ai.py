import streamlit as st

from pathlib import Path

import os
import requests

API_URL = os.getenv("MEDIASSIST_API_URL", "http://127.0.0.1:8000").rstrip("/")  ## this is the url of the backend API

# Redirect users to the main page if not logged in, otherwise continue to
# render the navigation menu
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

def get_file_list():
    """Fetch the list of files from the backend API."""
    try:
        response = requests.get(f"{API_URL}/files/list", timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching file list: {e}")
        return []

def delete_file(file_name):
    """Delete a file from the backend API."""
    try:
        response = requests.delete(f"{API_URL}/files/delete/{file_name}", timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        st.success(f"File {file_name} deleted successfully!")
    except requests.RequestException as e:
        st.error(f"Error deleting file {file_name}: {e}")

st.set_page_config(initial_sidebar_state=400)  # Width between 200 and 600 pixels

with st.sidebar:

    st.title("Files")

    file_list = []

    # 1. Initialize a unique identifier for the key in session state
    if "doc_uploader_key" not in st.session_state:
        st.session_state.doc_uploader_key = 0

    # Restrict file types in the interface.
    rag_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "txt"],
        max_upload_size=50,
        key=f"file_uploader_{st.session_state.doc_uploader_key}"
    )

    if rag_file is not None:
        # Check file size before saving or processing.
        max_bytes = 50 * 1024 * 1024

        if rag_file.size > max_bytes:
            st.error(
                f"The file exceeds the {50} MB limit."
            )
            st.stop()

        # Create a safe, application-controlled filename.
        extension = Path(rag_file.name).suffix.lower()
        supported_extensions = {".pdf", ".docx", ".txt"}

        if extension not in supported_extensions:
            st.error("Unsupported file type.")
            st.stop()

        try:
            # Prepare the file payload
            # Streamlit's UploadedFile object acts like a standard file-like object
            files = {"file": (rag_file.name, rag_file.getvalue(), rag_file.type)}
            response = requests.post(
                f"{API_URL}/files/upload", files=files, timeout=10
            )

            response.raise_for_status()  # Raise an error for bad responses
            st.success("File uploaded successfully!")
            # 3. Increment the key value to force a widget identity reset
            st.session_state.doc_uploader_key += 1
            
            # 4. Rerun the script to render the fresh, cleared widget
            st.rerun()
            file_list = get_file_list()
        except requests.HTTPError as error:
            detail = error.response.text if error.response is not None else str(error)
            st.error(f"The API rejected the request: {detail}")
        except requests.RequestException as error:
            st.error(f"Could not reach the API: {error}")

    with st.container(height=300):
        file_list = get_file_list()
        if file_list:
            st.write("Uploaded files:")
            col1, col2 = st.columns([4, 1])
            for file_name in file_list:
                col1.write(f"- {file_name}")
                col2.button(f"", 
                        key=f"delete_{file_name}", 
                        on_click=lambda f=file_name: delete_file(f),
                        icon=":material/delete:")
        else:
            st.write("No files uploaded yet.")
            

    # Restrict file types in the interface.
    image_file = st.file_uploader(
        "Choose a image file",
        type=[".jpg", ".jpeg", ".png"],
        max_upload_size=50
    )
    
    if image_file is not None:
        # Check file size before saving or processing.
        max_bytes = 50 * 1024 * 1024
    
        if image_file.size > max_bytes:
            st.error(
                f"The file exceeds the {50} MB limit."
            )
            st.stop()
    
        # Create a safe, application-controlled filename.
        extension = Path(image_file.name).suffix.lower()
        supported_extensions = {".jpg", ".jpeg", ".png"}
    
        if extension not in supported_extensions:
            st.error("Unsupported file type.")
            st.stop()


st.markdown(
    """
    <style>
            .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
                display: flex;
                flex-direction: row-reverse;
                align-itmes: end;
            }

            [data-testid="stChatMessageAvatarUser"] + [data-testid="stChatMessageContent"] * {
                text-align: right;
            }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("MediAssist AI Chatbot")

## Create a message history using session_state
## Streamlit will rerun this python script every time the user interacts with the application
## session_state will allow us to preserve the information between the reruns

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form("my_form", clear_on_submit=True):
    ## Input text box for the user
    user_input = st.text_input("Enter your question:")

    ## execute the generate_answer function by passing user query if the user press "ask" button
    if st.form_submit_button("Ask"):
        ## make sure the user input has some msg
        if user_input:
            payload = {"input": user_input}

            ## send the user question to the LLM
            try:
                response = requests.post(
                                f"{API_URL}/query", json=payload, timeout=10
                            )

                response.raise_for_status()  # Raise an error for bad responses

                ## Store the user question in session_state
                ## we store each message as a dictionary containing
                ## role: who sent the msg
                ## content: actual msg
                
                ## Store the LLM response in session_state
                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content": response.json().get("response", "No response from the model.")
                    }
                )

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": user_input
                    }
                )
                            
                user_input = ""  ## clear the input text box after the user press "ask" button

                # Keep the LAST 10 messages (most recent)
                trimmed_messages = st.session_state.messages[-10:]
                st.session_state.messages = trimmed_messages            
                
            except requests.HTTPError as error:
                detail = error.response.text if error.response is not None else str(error)
                st.error(f"The API rejected the request: {detail}")
            except requests.RequestException as error:
                st.error(f"Could not reach the API: {error}")

## Display the chat history
st.subheader("Chat history")

## loop through the message stored in session_state
for msg in st.session_state.messages[::-1]:
    # Display user message (CSS will force it to the right)
    with st.chat_message(msg['role']):
        st.markdown(f"{msg['content']}")