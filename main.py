import streamlit as st
from openai import OpenAI

st.title("Rememo - A document query assistant")

token = st.text_input("Enter your OpenAI API key", type="password")
if not token:
    st.stop()

client = OpenAI(api_key=token)

thread = client.beta.threads.create()

uploaded_file = st.file_uploader(
    "Upload a file", type=["txt", "pdf", "docx", "md"])
if uploaded_file is not None:
    st.write(uploaded_file.name)
    st.write(uploaded_file.type)
    st.write(uploaded_file.size)
    st.info("File uploaded successfully, now parsing...")
    file = client.files.create(
        file=uploaded_file.getvalue(), purpose='assistants')
    st.info(
        f"File parsed successfully, file id is {file.id}. now creating assistant...")

if not uploaded_file:
    st.stop()

assistant = client.beta.assistants.create(
    instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id]
)
st.info("Assistant created successfully, now creating a conversation...")


def get_response(prompt: str):
    st.info("Conversation created successfully, now sending message...")
    message = client.beta.threads.messages.create(
        thread.id,
        role='user',
        content=prompt
    )
    st.info("Message sent successfully, now running assistant...")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    st.info("Assistant ran successfully, now getting response...")
    messages = client.beta.threads.messages.list(thread.id)
    return messages


prompt = st.chat_input("Say something to the bot")
if prompt:
    st.info("Sending message...")
    messages = get_response(prompt)
    st.info("Message sent successfully, now receiving response...")
    print(messages)
