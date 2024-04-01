get_tasks_schema = {
    "name": "getTasks",
    "description": "Get (unfinished) tasks from Todoist",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

add_tasks_schema = {
    "name": "addTasks",
    "description": "Add multiple tasks to Todoist",
    "parameters": {
        "type": "object",
        "properties": {
            "tasks": {
                "type": "array",
                "description": "List of tasks that needs to be added to the Todoist",
                "items": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Format: task description"
                        },
                        "due_string": {
                            "type": "string",
                        }
                    }
                }
            }
        }
    }
}

finish_tasks_schema = {
    "name": "closeTasks",
    "description": "Finish/Complete tasks in Todoist",
    "parameters": {
        "type": "object",
        "properties": {
            "tasks": {
                "type": "array",
                "description": "List of IDs of tasks that needs to be finished/completed",
                "items": {
                    "type": "number",
                }
            }
        }
    }
}

update_tasks_schema = {
    "name": "updateTasks",
    "description": "Update multiple tasks in Todoist based on the current tasks mentioned in the conversation",
    "parameters": {
        "type": "object",
        "properties": {
            "tasks": {
                "type": "array",
                "description": "List of tasks that needs to be updated in the Todoist",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "number",
                            "description": "ID of the task to update"
                        },
                        "content": {
                            "type": "string",
                            "description": "Format: task description"
                        },
                        "due_string": {
                            "type": "string",
                        }
                    }
                }
            }
        }
    }
}
