
# What is AI DEVS 2
Let's quothe the autors =)
```
AI_Devs to 5-tygodniowy, największy w Polsce, kurs łączenia narzędzi Generative AI 
(w szczególności modeli OpenAI) z logiką aplikacji oraz narzędziami do automatyzacji. 
Całkowicie rezygnujemy z ChatGPT na rzecz bezpośredniego połączenia z modelami poprzez
API, budując dopasowane narzędzia zwiększające efektywność codziennych zadań.
```

####  Progress [C05L01/C05L05]: 
![84%](https://geps.dev/progress/84)


# What is THIS REPO?
This is everything related to the course that I am doing during learning.

It will contains few modules:
| Module | Description |
| --- | --- |
| [examples_python](examples_python) | python implementations of optional course examples covering OpenAI, Langchain, vector databases, and similarity search. The goal is to recreate the functionality presented in TS examples with Python. |
| [api_tasks](api_tasks) | python implementations of tasks required to complete this course. |
| [chat_tasks](chat_tasks) | tasks completed on the course platform (which simulates a modified OpenAI playground). Contains a task descriptions and list of my attempts for future reference. |
| [docs](docs) | Additional descriptions and theory researched and documented while completing the course. Generaly things useful for future reference in upcoming examples, produced while i was processing knowledge. |
| [own_testing](own_testing) | some kind of sandbox with additional tests, libraries and methods methods comparations and trying different ways to achieve the same goals, kept for reference. |


# Personal Notes, Tests, and Examples (doc + own_testing)
| Lesson | Name | Description |
| --- | --- | --- |
| C01L04 | PYTHON 🐍<br>[different_connections_to_openai.py](own_testing/C01L04_different_connections_to_openai.py) | - Different ways to connect with OpenAI models using the OpenAI library and the requests library<br>    - Streaming example that prints the content of the response chunk by chunk as it is generated<br>    - Example of using the LangChain library to initialize a default model (gpt-3.5-turbo)<br>     |
| C01L04 | PYTHON 🐍<br>[langchain_conversationchain.py](own_testing/C01L04_langchain_conversationchain.py) | - Two ways to create a conversation using the LangChain library with the OpenAI chat model<br>    - The first method manually creates a list to hold message objects (HumanMessage, SystemMessage, AIMessage) and appends them to the list as the conversation progresses<br>    - The second method uses the ConversationChain class implemented in LangChain, which automatically manages the conversation history using ConversationBufferMemory<br>    - Both methods allow for sending messages to the model and receiving responses, maintaining the context of the conversation<br>     |
| C03L01 | MARKDOWN 📜<br>[async.md](docs/C03L01_async.md) | - Event loop in Python and its usage in Jupyter/interactive mode vs normal scripts<br>    - Document objects in langchain library<br>    - Sync (model.invoke) vs async (model.agenerate) methods for chat models<br>    - Code examples of async workflow with asyncio.gather<br>     |
| C03L01 | MARKDOWN 📜<br>[simulating_max_cocurrency.md](docs/C03L01_simulating_max_cocurrency.md) | - Python's langchain library doesn't have a direct equivalent of the maxConcurrency parameter for the ChatOpenAI class<br>    - Concurrency can be controlled using Python's asyncio library and semaphores<br>    - The text provides a possible solution using asyncio.Semaphore to limit concurrency when generating descriptions for multiple documents<br>     |
| C03L03 | MARKDOWN 📜<br>[FAISS_vetor_storing.md](docs/C03L03_FAISS_vetor_storing.md) | - FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors<br>    - It converts data into high-dimensional vectors using embeddings or feature extraction techniques<br>    - FAISS creates an index to enable fast similarity search by organizing the vectors for efficient retrieval<br>    - The pre-built index allows for quick similarity search when a query vector is provided, using optimized algorithms and parallelization to speed up the process<br>     |
| C03L03 | JUPYTER NOTEBOOK 🐍+📜<br>[function_calling.ipynb](own_testing/C03L03_function_calling.ipynb) | - How to prepare functions and their schemas to be used with LLMs for function calling<br>    - Different ways to initialize models with function schemas using dictionaries, pydantic BaseModel or convert_to_openai_tool<br>    - Extracting function names and arguments from the model's response<br>    - Executing the selected function with the provided arguments<br>    - Comparison of function calling and prompt-with-examples approaches for solving a specific task<br>     |
| C04L04 | JUPYTER NOTEBOOK 🐍+📜<br>[C04L04_README.md](/api_tasks/C04L04/C04L04_README.md) | - How we can host FLASK API and use ngrok to tunnel traffic to our local hosting<br>    - The process involves preparing a function to generate answers using LLM, creating a Flask API to handle user requests and return answers, and using ngrok to make the locally running app accessible over the internet<br>    - The text provides step-by-step instructions on how to set up the Flask API, configure ngrok, and complete the task by executing parts of the C04L04_ownapi.py file while the API is running<br>     |


# Examples from lessons
Orginally available in typescript at https://github.com/i-am-alice/2nd-devs/
| Name | python version | typescript | typescript | status |
| --- | --- | --- | --- | --- |
| 01_langchain_init | [Python](examples_python/01_langchain_init/01.py) |[snapshot](examples_python/01_langchain_init/01.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/01_langchain_init/01.ts) | ✅DONE |
| 02_langchain_format | [Python](examples_python/02_langchain_format/02.py) |[snapshot](examples_python/02_langchain_format/02.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/02_langchain_format/02.ts) | ✅DONE |
| 03_langchain_stream | [Python](examples_python/03_langchain_stream/03.py) |[snapshot](examples_python/03_langchain_stream/03.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/03_langchain_stream/03.ts) | ✅DONE |
| 04_tiktoken | [Python](examples_python/04_tiktoken/04.py) |[snapshot](examples_python/04_tiktoken/04.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/04_tiktoken/04.ts) | ✅DONE |
| 05_conversation | [Python](examples_python/05_conversation/05.py) |[snapshot](examples_python/05_conversation/05.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/05_conversation/05.ts) | ✅DONE |
| 06_external | [Python](examples_python/06_external/06.py) |[snapshot](examples_python/06_external/06.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/06_external/06.ts) | ✅DONE |
| 07_output | [Python](examples_python/07_output/07.py) |[snapshot](examples_python/07_output/07.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/07_output/07.ts) | ✅DONE |
| 08_cot | [Python](examples_python/08_cot/08.py) |[snapshot](examples_python/08_cot/08.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/08_cot/08.ts) | ✅DONE |
| 09_context | [Python](examples_python/09_context/09.py) |[snapshot](examples_python/09_context/09.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/09_context/09.ts) | ✅DONE |
| 10_switching | [Python](examples_python/10_switching/10.py) |[snapshot](examples_python/10_switching/10.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/10_switching/10.ts) | ✅DONE |
| 11_docs | [Python](examples_python/11_docs/11.py) |[snapshot](examples_python/11_docs/11.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/11_docs/11.ts) | ✅DONE |
| 12_web | [Python](examples_python/12_web/12.py) |[snapshot](examples_python/12_web/12.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/12_web/12.ts) | ✅DONE |
| 13_functions | [Python](examples_python/13_functions/13.py) |[snapshot](examples_python/13_functions/13.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/13_functions/13.ts) | ✅DONE |
| 14_agent | [Python](examples_python/14_agent/14.py) |[snapshot](examples_python/14_agent/14.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/14_agent/14.ts) | ✅DONE |
| 15_tasks | [Python](examples_python/15_tasks/15.py) |[snapshot](examples_python/15_tasks/15.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/15_tasks/15.ts) | ✅DONE |
| 16_nocode | [Python](examples_python/16_nocode/16.py) |[snapshot](examples_python/16_nocode/16.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/16_nocode/16.ts) | ✅DONE |
| 17_tree | [Python](examples_python/17_tree/17.py) |[snapshot](examples_python/17_tree/17.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/17_tree/17.ts) | ✅DONE |
| 18_knowledge | [Python](examples_python/18_knowledge/18.py) |[snapshot](examples_python/18_knowledge/18.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/18_knowledge/18.ts) | ✅DONE |
| 19_llama | [Python](examples_python/19_llama/19.py) |[snapshot](examples_python/19_llama/19.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/19_llama/19.ts) | ❌WAITING |
| 20_catch | [Python](examples_python/20_catch/20.py) |[snapshot](examples_python/20_catch/20.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/20_catch/20.ts) | ✅DONE |
| 21_similarity | [Python](examples_python/21_similarity/21.py) |[snapshot](examples_python/21_similarity/21.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/21_similarity/21.ts) | ✅DONE |
| 22_simple | [Python](examples_python/22_simple/22.py) |[snapshot](examples_python/22_simple/22.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/22_simple/22.ts) | ✅DONE |
| 23_fragmented | [Python](examples_python/23_fragmented/23.py) |[snapshot](examples_python/23_fragmented/23.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/23_fragmented/23.ts) | ✅DONE |
| 24_files | [Python](examples_python/24_files/24.py) |[snapshot](examples_python/24_files/24.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/24_files/24.ts) | ✅DONE |
| 25_correct | [Python](examples_python/25_correct/25.py) |[snapshot](examples_python/25_correct/25.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/25_correct/25.ts) | ✅DONE |
| 26_summarize | [Python](examples_python/26_summarize/26.py) |[snapshot](examples_python/26_summarize/26.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/26_summarize/26.ts) | ✅DONE |
| 27_qdrant | [Python](examples_python/27_qdrant/27.py) |[snapshot](examples_python/27_qdrant/27.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/27_qdrant/27.ts) | ✅DONE |
| 28_intent | [Python](examples_python/28_intent/28.py) |[snapshot](examples_python/28_intent/28.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/28_intent/28.ts) | ✅DONE |
| 29_notify | [Python](examples_python/29_notify/29.py) |[snapshot](examples_python/29_notify/29.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/29_notify/29.ts) | ✅DONE |
| 30_youtube | [Python](examples_python/30_youtube/30.py) |[snapshot](examples_python/30_youtube/30.py) | [orginal](https://github.com/i-am-alice/2nd-devs/blob/main/30_youtube/30.ts) | ✅DONE |

# Api tasks
| CHAPTER/LESSON | Task | Tags | Description |
| --- | --- | --- | --- |
| C01L01 | [C01L01_helloapi.py](api_tasks/C01L01_helloapi.py) | [course_api_only] | Testing api to connect with course platform |
| C01L04 | [C01L04_blogger.py](api_tasks/C01L04_blogger.py) | [OpenAI] | Base connection with OpenAI |
| C01L04 | [C01L04_moderation.py](api_tasks/C01L04_moderation.py) | [OpenAI][Guard] | openai/moderations endpoint (to prevent user input make us banned) |
| C01L05 | [C01L05_liar.py](api_tasks/C01L05_liar.py) | [Guard] | Very basic example of checking if input/api response looks like we expected |
| C02L02 | [C02L02_inprompt.py](api_tasks/C02L02_inprompt.py) | [langchain][pandas] | Example of filtering longer data to provide valuable context for model |
| C02L03 | [C02L03_embedding.py](api_tasks/C02L03_embedding.py) | [OpenAI] | openai/embeddings endpoint - example of convertig text to numbers |
| C02L04 | [C02L04_whisper.py](api_tasks/C02L04_whisper.py) | [OpenAI][whisper] | Example of generating transcriptions |
| C02L05 | [C02L05_functions.py](api_tasks/C02L05_functions.py) | [course_api_only] | Example of writing function definition for openai |
| C03L01 | [C03L01_rodo.py](api_tasks/C03L01_rodo.py) | [course_api_only] | Example of writing prompt that will suggest model to do something |
| C03L02 | [C03L02_scraper.py](api_tasks/C03L02_scraper.py) | [langchain][webscrap] | Example of trying to gather data from server that may have some basic prevention/random errors |
| C03L03 | [C03L03_whoami.py](api_tasks/C03L03_whoami.py) | [langchain][ConversationChain] | Task to practice with store chat history/using ConversationChain |
| C03L04 | [C03L04_search.py](api_tasks/C03L04_search.py) | [qdrant][embeddings][similarity search][vector database] | Embeddings creation, indexation and performing similarity search for dynamic context generation for LLM with qdrant |
| C03L05 | [C03L05_people.py](api_tasks/C03L05_people.py) | [pandas][langchain][filtering data] | Filtering only desired context for llm (in my case using PANDAS DATAFRAME) |
| C04L01 | [C04L01_knowledge.py](api_tasks/C04L01_knowledge.py) | [function calling][langchain][apis] | Connecting to different APIs basing on LLM decision (with function_calling) |
| C04L02 | [C04L02_tools.py](api_tasks/C04L02_tools.py) | [function_calling][langchain] | Another function_calling example to get correct json (Letting LLM determine incoming action). Also, adding extra systempromt with context to let model understand dates. |
| C04L03 | [C04L03_gnome.py](api_tasks/C04L03_gnome.py) | [langchain][vison][analyzing images] | Example using Vision model to let model analyze content of some image |
| C04L04 | [C04L04_ownapi.py](api_tasks/C04L04_ownapi.py) | [langchain][api][flask][ngrok] | Create app that will catch post requests, extract user question and get answer from LLM |
| C04L05 | [C04L05_ownapipro.py](api_tasks/C04L05_ownapipro.py) | [langchain][ConversationChain][api][flask][ngrok] | Create app that will catch post requests, extract user question and get answer from LLM while holding user messages in memory |
| C05L01 | [C05L01_meme.py](api_tasks/C05L01_meme.py) | [RenderForm][documents from templates] | Use renderform prepare template and generate images basing on this template |


# Chat_tasks
They are saved mostly for searching for specific prompt examples.
I didn't see any reason to keep then in separated files so they are all available [here](chat_tasks/chat_tasks.md)
| Lesson | Name | Description | status |
| --- | --- | --- | --- |
| C01L01 | [getinfo](chat_tasks/chat_tasks.md/#C01L01---getinfo) | Forcing ChatGPT to output the word BANANA without using that word in the prompt. Difficulties - some words are disabled in the prompt. | ✅DONE |
| C01L02 | [maxtokens](chat_tasks/chat_tasks.md/#C01L02---maxtokens) | Providing the name of a river flowing through the capital of a given country, while staying within the max token limit. | ✅DONE |
| C01L03 | [category](chat_tasks/chat_tasks.md/#C01L03---category) | Making ChatGPT assign an appropriate category (home/work/other) to a task and return the answer in JSON format. | ✅DONE |
| C01L03 | [books](chat_tasks/chat_tasks.md/#C01L03---books) | Preparing a JSON array with book titles and authors using one-shot prompting with GPT-3.5-turbo. | ✅DONE |
| C01L05 | [injection injection2](chat_tasks/chat_tasks.md/#C01L05---injection-injection2) | Using prompt injection to extract a secret word from the prompt, with increasing difficulty levels and models (GPT-3.5 and GPT-4). | ✅DONE |
| C02L01 | [optimize](chat_tasks/chat_tasks.md/#C02L01---optimize) | Defining the 'system' field in a query to perform a given task while staying within the character limit, which is more challenging than token limit. | ✅DONE |
| C02L01 | [fixit](chat_tasks/chat_tasks.md/#C02L01---fixit) | Convincing GPT-4 to fix and optimize provided source code, handle errors properly, and return zero for all incorrect inputs. | ✅DONE |
| C02L02 | [parsehtml](chat_tasks/chat_tasks.md/#C02L02---parsehtml) | Extracting readable article text from HTML code (in paragraphs), converting it to Markdown format, and returning only the three paragraphs without any HTML code. | ✅DONE |
| C02L03 | [structure](chat_tasks/chat_tasks.md/#C02L03---structure) | Preparing a prompt that works with both GPT-3.5-Turbo and GPT-4 models to generate a JSON object with a specific structure, taking into account the strengths and weaknesses of GPT-3.5-Turbo. | ✅DONE |
| C02L05 | [cities](chat_tasks/chat_tasks.md/#C02L05---cities) | Generating a list of 7 interesting facts about a given city without using the city name in the prompt or the generated response, while working with the GPT-3.5-turbo model. | ✅DONE |
| C03L01 | [tailwind](chat_tasks/chat_tasks.md/#C03L01---tailwind) | Writing a system message that returns a `<button>` element consistent with the user's message, ensuring the model's response contains only the `<button>` element without additional comments or tags. | ✅DONE |
| C03L02 | [format](chat_tasks/chat_tasks.md/#C03L02---format) | Creating a converter from an old African markup language to HTML code, instructing GPT-3.5-turbo on how to handle and interpret the code. | ✅DONE |
| C03L05 | [planets](chat_tasks/chat_tasks.md/#C03L05---planets) | Generating a JSON array consisting of 9 planet names in the solar system (including Pluto), with names in lowercase Polish, without mentioning planets, solar system, JSON, or the Polish language in the prompt. | ✅DONE |

