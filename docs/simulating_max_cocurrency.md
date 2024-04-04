# Python langchain has no implemented 
In the Python version of Langchain, there isn't a direct equivalent of the maxConcurrency parameter for the ChatOpenAI class. However, you can achieve a similar effect by controlling the concurrency of your async operations using Python's asyncio library.

When you use asyncio.gather() to run multiple async operations concurrently, you can limit the number of concurrent operations by creating a semaphore. A semaphore is a synchronization primitive that allows you to control the number of tasks that can access a shared resource simultaneously.

It is mentioned in https://api.python.langchain.com/en/latest/chat_models/langchain_community.chat_models.openai.ChatOpenAI.html and https://python.langchain.com/docs/integrations/llms/ but i wasn't able to make it work for now
- asyncio.gather throws an error: 
- TypeError: AsyncCompletions.create() got an unexpected keyword argument 'max_concurrency'

# Possible solution
Adding semaphore to function to limit concurency that way
```python
import asyncio
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

model = ChatOpenAI()
semaphore = asyncio.Semaphore(5)  # Limit concurrency to 5

async def generate_description(doc):
    async with semaphore:
        system_message = SystemMessage(content="""
            Describe the following document with one of the following keywords:
            Mateusz, Jakub, Adam. Return the keyword and nothing else.
        """)
        human_message = HumanMessage(content=f'Document: {doc.page_content}')
        return await model.agenerate([[system_message], [human_message]])

description_promises = [generate_description(doc) for doc in documents]
descriptions = await asyncio.gather(*description_promises)
``````