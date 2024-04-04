from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from helper import current_date, parse_function_call, rephrase
from todoist import add_tasks, close_tasks, list_uncompleted, update_tasks
from schema import add_tasks_schema, finish_tasks_schema, get_tasks_schema, update_tasks_schema

model = ChatOpenAI(model_name="gpt-4-turbo-preview", model_kwargs={"functions": [get_tasks_schema, add_tasks_schema, finish_tasks_schema, update_tasks_schema]})
tools = {"getTasks": list_uncompleted, "addTasks": add_tasks, "closeTasks": close_tasks, "updateTasks": update_tasks}

async def act(query: str) -> str:
    print('User:', query)
    tasks = await list_uncompleted()
    conversation = await model.agenerate([[
        SystemMessage(content=f"""
            Fact: Today is {current_date()}
            Current tasks: ###{''.join(task.content + ' (ID: ' + str(task.id) + ')' for task in tasks)}###"""),
        HumanMessage(content=query),
    ]])
    action = parse_function_call(conversation.generations[0][0].message)
    response = ''
    if action:
        print(f"action: {action['name']}")
        response_tasks = await tools[action['name']](action['args']['tasks'])
        response_str = ', '.join(f"{task.content} (ID: {task.id})" for task in response_tasks)
        response = await rephrase(response_str, query)
    else:
        response = conversation.generations[0][0].text
    print(f"AI: {response}\n")
    return response


query = 'Need to buy milk, add it to my tasks'
await act('I need to write a newsletter about gpt-4 on Monday, can you add it?')
await act('Need to buy milk, add it to my tasks')
await act('Ouh I forgot! Beside milk I need to buy sugar. Update my tasks please.')
await act('Get my tasks again.')
await act('Dodaj mi na jutro do zadań zrobienie zakupów i odhaczenie lekcji numer 11')
