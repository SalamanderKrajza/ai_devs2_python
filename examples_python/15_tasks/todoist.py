import os
import json
from typing import List, Dict, Union
from todoist_dt import ITask, ITaskClose, ITaskModify, IDue
import aiohttp
import asyncio

async def api_call(endpoint: str = '/me', method: str = 'GET', body: Dict = None) -> Union[bool, Dict]:
    if body is None:
        body = {}
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.environ["TODOIST_API_KEY"]}'
        }
        async with aiohttp.ClientSession() as session:
            if method == 'POST':
                async with session.post(f'https://api.todoist.com/rest/v2{endpoint}', headers=headers, json=body) as response:
                    if response.status == 204:
                        return True
                    return await response.json()
            else:
                async with session.get(f'https://api.todoist.com/rest/v2{endpoint}', headers=headers) as response:
                    return await response.json()
    except Exception as err:
        print(err)

async def list_uncompleted() -> List[ITask]:
    uncompleted = await api_call('/tasks', 'GET')
    return [ITask(
        id=task['id'],
        assigner_id=None,
        assignee_id=None,
        project_id=task['project_id'],
        section_id=None,
        parent_id=None,
        order=0,
        content=task['content'],
        description='',
        is_completed=False,
        labels=[],
        priority=0,
        comment_count=0,
        creator_id=task['creator_id'],
        created_at=task['created_at'],
        due=IDue(
            date=task['due'].get('date', ''),
            timezone=task['due'].get('timezone', ''),
            string=task['due'].get('string', ''),
            lang=task['due'].get('lang', ''),
            is_recurring=task['due'].get('is_recurring', False),
            datetime=task['due'].get('datetime', '')
        ) if task.get('due') else None,
        url=task['url'],
        duration=None
    ) for task in uncompleted]


async def add_tasks(tasks: List[Union[ITaskModify, Dict]]) -> List[ITaskModify]:
    promises = [api_call('/tasks', 'POST', {
        'content': task['content'] if isinstance(task, dict) else task.content,
        'due_string': task.get('due_string') if isinstance(task, dict) else task.due_string
    }) for task in tasks]

    added_tasks = await asyncio.gather(*promises)

    return [ITaskModify(
        id=added_task['id'],
        content=added_task['content'],
        due_string=added_task['due']['string'] if added_task['due'] else None
    ) for added_task in added_tasks]


async def update_tasks(tasks: List[ITaskModify]) -> List[ITaskModify]:
    promises = [api_call(f'/tasks/{task.id}', 'POST', {
        'content': task.content,
        'due_string': task.due_string,
        'is_completed': task.is_completed
    }) for task in tasks]

    updated_tasks = await asyncio.gather(*promises)

    return [ITaskModify(
        id=updated_task['id'],
        content=updated_task['content'],
        due_string=updated_task['due']['string'] if updated_task['due'] else None
    ) for updated_task in updated_tasks]

async def close_tasks(tasks: List[ITaskClose]) -> Union[List[Dict[str, str]], str]:
    promises = [api_call(f'/tasks/{task.id}/close', 'POST') for task in tasks]

    try:
        await asyncio.gather(*promises)
        return [{str(closed_task.id): 'completed'} for closed_task in tasks]
    except Exception:
        return 'No tasks were closed (maybe they were already closed)'
