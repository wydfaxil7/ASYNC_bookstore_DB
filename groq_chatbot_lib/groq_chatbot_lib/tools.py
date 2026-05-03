from typing import Optional


class ToolParameter:
    def __init__(
        self,
        name: str,
        type: str,
        description: str,
        required: bool = True,
        enum: Optional[list] = None
    ):
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.enum = enum

    def to_schema(self) -> dict:
        schema = {
            "type": self.type,
            "description": self.description
        }
        if self.enum:
            schema["enum"] = self.enum
        return schema


class ToolDefinition:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Optional[list] = None
    ):
        self.name = name
        self.description = description
        self.parameters = parameters or []

    def to_groq_format(self) -> dict:
        required_params = [
            p.name for p in self.parameters if p.required
        ]
        properties = {
            p.name: p.to_schema()
            for p in self.parameters
        }
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params
                }
            }
        }


class ToolCall:
    def __init__(self, id: str, name: str, arguments: dict):
        self.id = id
        self.name = name
        self.arguments = arguments


class ToolResult:
    def __init__(
        self,
        tool_call_id: str,
        content: str,
        is_error: bool = False
    ):
        self.tool_call_id = tool_call_id
        self.content = content
        self.is_error = is_error

    def to_groq_message(self) -> dict:
        return {
            "role": "tool",
            "tool_call_id": self.tool_call_id,
            "content": self.content
        }