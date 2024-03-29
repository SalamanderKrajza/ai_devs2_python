#############################################################################
# ------------- EVENT LOOP and interactive window
#############################################################################

    # --------------------------- IMPORTANT -------------------------------
    # THIS CODE IS PREPARED TO WORK ON JUPYTER NOTEBOOK OR INTERACTIVE MODE

    # EVENT LOOP 
        # in jupyter/interactive mode it possible to keep code "alive" and wait for another user input (event) to process
        # allows running multiple coroutines (async functions) concurrently on a single thread.

    # In Jupyter/interactive mode, you are already inside an EVENT LOOP managed by IPython. So you don't need to explicitly start the event loop using asyncio.run() or loop.run_until_complete().
    # In a normal Python script, there is no pre-existing event loop, so you need to start one explicitly to run async code. This is typically done by calling asyncio.run(main()) where main() is an async function that serves as the entry point.
    # To write async code that works in both interactive and normal mode, you can use a pattern like this:

    # Example of implementation to make it work in both modes (interactive/normal)

            # import asyncio

            # async def main():
            #     # Your async code here
            #     await asyncio.sleep(1)
            #     print("Async task done")

            # if __name__ == "__main__":
            #     asyncio.run(main())
            # else:
            #     # For Jupyter/interactive
            #     await main()
 
    # NOTE - In case you need to specify create new async loop 
    # (not just wait for task to process async but something more advanced)
    # you may need to check nest_asyncio or %%script ipython


#############################################################################
# ------------- Some theory needed to working with langchain and async
#############################################################################
# --------------------------------------------------------------
# doc objects
# --------------------------------------------------------------
    # The langchain library uses Document objects to represent chunks of text data.
    # A Document has a page_content attribute that stores the actual text.
    # Using Document objects allows associating metadata with the text, which is useful for tracking provenance, splitting documents into chunks, etc.
    # So while you could use a list of strings, Document objects provide a more structured way to work with text data in langchain.

# --------------------------------------------------------------
# Coroutine object (functions executed with async)
# --------------------------------------------------------------
    # Coroutines are functions defined with async def that return coroutine objects when called.
    # Unlike regular functions, calling a coroutine function does not execute the body, it just creates a coroutine object.
    # The body is executed only when the coroutine is explicitly awaited or scheduled to run on an event loop.
    # Coroutines can be suspended at await points, allowing cooperative multitasking without threads.
    # Coroutines are a key building block for writing asynchronous code in Python

# --------------------------------------------------------------
# model.invoke vs model.agenerate (sync vs async)
# --------------------------------------------------------------
    # model.invoke is a synchronous method to send a list of messages to the chat model and get the result.
    # model.agenerate is the asynchronous equivalent that returns a coroutine object which needs to be awaited.
    # agenerate allows running multiple requests concurrently to improve performance.
    # invoke is simpler to use for sequential code, while agenerate is better suited inside async functions.7

#############################################################################
# ------------- EXAMPLE TO USE ASYNC VERSION OF FUNCTIONS
#############################################################################
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
model = ChatOpenAI()
docs = [
    'Adam has various skills but describes himself as "just curious."',
    'Adam have a dog named Alexa.'
]
system_message = SystemMessage(content="""
    Describe the following document with one of the following keywords:
    Mateusz, Jakub, Adam. Return the keyword and nothing else.
""")
human_message = HumanMessage(content=f'Document: {docs[0]}')

# --------------------------------------------------------------
# version using sync
# --------------------------------------------------------------
# Long version - often seen on examples
test_sync = model.invoke(messages=[system_message, human_message]).content
# Shortened version of exactly the same code
test_sync = model([system_message, human_message]).content
print(test_sync)

# --------------------------------------------------------------
# Using agenerate with 1 sample to show async variant
# --------------------------------------------------------------

# Generate function that wait for start
promise = model.agenerate(messages=[[system_message, human_message]])
# Run generated coroutine (async function)
test_async = await promise
# Print result for conversation number = 0 and version of output number = 0
print(test_async.generations[0][0].text)

# --------------------------------------------------------------
# using agenerate to present final workflow
# --------------------------------------------------------------
import asyncio

promises = []
for doc in docs:
    system_message = SystemMessage(content="""
    Describe the following document with one of the following keywords:
    Mateusz, Jakub, Adam. Return the keyword and nothing else.
""")
    human_message = HumanMessage(content=f'Document: {doc}')
    # add function object with arguments (it need to be called later) 
    promises.append(model.agenerate(messages=[[system_message, human_message]]))

# use asyncio.gather to call all functions (promises) at the same time
test_async = await asyncio.gather(*promises)

# We may provide list of promises (functions) and get multiple model responses
for model_response in test_async:
    # We may provide list of conversation and get multiple responses
    for single_conversation_response in model_response.generations: 
        # We may use n=2 or more in model.agenerate to get multiple responses for same prompt
        for output in single_conversation_response:
            print(output.text)

#############################################################################
# ------------- Final piece of code to simulate typescript example
#############################################################################
import json
import asyncio
from langchain.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from langchain.schema import HumanMessage, SystemMessage

loader = TextLoader("docs.md")
doc = loader.load()[0]
documents = [Document(page_content=content) for content in doc.page_content.split("\n\n")]
print(documents)

from langchain_core.runnables.config import RunnableConfig

model = ChatOpenAI()

async def generate_description(doc):
    system_message = SystemMessage(content="""
        Describe the following document with one of the following keywords:
        Mateusz, Jakub, Adam. Return the keyword and nothing else.
    """)
    human_message = HumanMessage(content=f'Document: {doc.page_content}')
    return await model.agenerate([[system_message], [human_message]])


description_promises = [generate_description(doc) for doc in documents]
descriptions = await asyncio.gather(*description_promises)

for index, description in enumerate(descriptions):
    documents[index].metadata["source"] = description.generations[0][0].text

with open("docs.json", "w") as f:
    json.dump([doc.dict() for doc in documents], f, indent=2)

