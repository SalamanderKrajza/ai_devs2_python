##################################################
# ------------- Example2 from Course - użycie ChagPromptTemplate
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

# Zwykle do definiowania promptów warto korzystać z template strings
# Tutaj treści zamknięte w klamrach {} są zastępowane przez LangChain konkretnymi wartościami
context = """
The Vercel AI SDK is an open-source library designed to help developers build conversational, streaming, and chat user interfaces in JavaScript and TypeScript. The SDK supports React/Next.js, Svelte/SvelteKit, with support for Nuxt/Vue coming soon.
To install the SDK, enter the following command in your terminal:
npm install ai
"""
system_template = """
As a {role} who answers the questions ultra-concisely using CONTEXT below 
and nothing more and truthfully says "don't know" when the CONTEXT is not enough to give an answer.

context###{context}###
"""
human_template = "{text}"

# Utworzenie promptu z dwóch wiadomości według podanych szablonów:
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template),
])

# Faktyczne uzupełnienie szablonów wartościami
formatted_chat_prompt = chat_prompt.format_messages(
    context=context,
    role="Senior JavaScript Programmer",
    text="What is Vercel AI?",
)

# Inicjalizacja domyślnego modelu, czyli gpt-3.5-turbo
chat = ChatOpenAI()
# Wykonanie zapytania do modelu
response = chat.invoke(formatted_chat_prompt)

# Wyświetlenie odpowiedzi
print(response.content)


##################################################
# ------------- Example2 from Course - BEZ ChatPromptTemplate
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

#Generuj wiadomosc sytemu
context = """
The Vercel AI SDK is an open-source library designed to help developers build conversational, streaming, and chat user interfaces in JavaScript and TypeScript. The SDK supports React/Next.js, Svelte/SvelteKit, with support for Nuxt/Vue coming soon.
To install the SDK, enter the following command in your terminal:
npm install ai
"""
role = "Senior JavaScript Programmer"

system_message = f"""
As a {role} who answers the questions ultra-concisely using CONTEXT below 
and nothing more and truthfully says "don't know" when the CONTEXT is not enough to give an answer.

context###{context}###
"""

#Generuj wiadomosc czlowieka
human_message = "What is Vercel AI?"

# odpowiedź
chat = ChatOpenAI()
response = chat.invoke([
    SystemMessage(system_message),
    HumanMessage(human_message),
])

# Wyświetlenie odpowiedzi
print(response.content)