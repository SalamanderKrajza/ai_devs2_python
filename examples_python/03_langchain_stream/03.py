##################################################
# ------------- Example3 from Course - streaming
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage

from langchain_core.callbacks import BaseCallbackHandler
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"My custom handler, token: {token}")

# Inicjalizacja chatu z włączonym streamingiem
chat = ChatOpenAI(streaming=True, callbacks=[MyCustomHandler()])

# Wywołanie chatu wraz z funkcją przyjmującą kolejne tokeny składające się na wypowiedź modelu
chat.invoke([
    HumanMessage(
        "Hey there!"
    ),
])