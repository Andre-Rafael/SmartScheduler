from datetime import datetime
from logging import info
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
import uvicorn
from schemas.response import ResponseSchema
from schemas.schedule_data import ScheduleData  


app = FastAPI()
load_dotenv(r"../.env")
print(os.environ.get("GOOGLE_API_KEY"))

chat_google_gen_ai = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

store = {}


@app.get("/")
async def main():
    return {
        "message": """Olá! 👋 Bem-vindo(a) ao SmartSchedule! 🤖 Sou o seu novo agente de IA, projetado para simplificar sua vida.
            Minha missão é transformar qualquer texto que você me enviar em um link de agendamento rápido e fácil. 
            Diga adeus à complicação! 📅✨
            É só me dizer o que você precisa agendar. Estou pronto para começar!
            🚀 Como posso te ajudar a agendar seu tempo hoje?"""
    }


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        info(store[session_id])
    return store[session_id]


@app.post(path="/check_event", response_model=ResponseSchema)
async def schedule(user_input: ScheduleData):
    template = """
        You are a helpful assistant that create a event generating a link to create in google calendar. 
        Today is {current_date} and the history of the conversation is: {history}.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(template),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{user_input}"),
        ]
    )
    info(user_input.text)
    chain = prompt | chat_google_gen_ai

    chat_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="user_input",
        history_messages_key="history",
    )

    response = chat_with_history.invoke(
        {
            "user_input": user_input.text,
            "current_date": datetime.now().strftime("%Y-%m-%d"),
        },
        config={"configurable": {"session_id": user_input.id}},
    )
    return ResponseSchema(id=user_input.id, text=response.content)


if __name__ == "__main__":
    uvicorn.main(app, host="0.0.0.0", port=8000)
