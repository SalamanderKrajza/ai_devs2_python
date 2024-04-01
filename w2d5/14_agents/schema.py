multiply_schema = {
    "name": "multiply",
    "description": "Multiply two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "first": {
                "type": "number",
                "description": "First value to multiply"
            },
            "second": {
                "type": "number",
                "description": "Second value to multiply"
            }
        },
        "required": [
            "first", "second"
        ]
    }
}

add_schema = {
    "name": "add",
    "description": "Add two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "first": {
                "type": "number",
                "description": "First value to add"
            },
            "second": {
                "type": "number",
                "description": "Second value to add"
            }
        },
        "required": [
            "first", "second"
        ]
    }
}

subtract_schema = {
    "name": "subtract",
    "description": "Subtract two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "first": {
                "type": "number",
                "description": "First value to subtract"
            },
            "second": {
                "type": "number",
                "description": "Second value to subtract"
            }
        },
        "required": [
            "first", "second"
        ]
    }
}
