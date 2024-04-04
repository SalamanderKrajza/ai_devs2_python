import sys
sys.path.append(r'..')
from dotenv import load_dotenv
load_dotenv()

##################################################
# ------------- Example1 from Course - LangChain INIT
##################################################
# Importowanie odpowiednich klas
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage

# Inicjalizacja domyślnego modelu, czyli gpt-3.5-turbo
chat = ChatOpenAI()

# Wywołanie modelu poprzez przesłanie tablicy wiadomości.
# W tym przypadku to proste przywitanie
response = chat.invoke([
    HumanMessage("Hey there!")
])

# Wyświetlenie odpowiedzi
print(response.content)