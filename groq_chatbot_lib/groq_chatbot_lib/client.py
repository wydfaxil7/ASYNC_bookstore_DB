import json
import asyncio
from typing import Optional, Callable, Awaitable
from groq import Groq
from groq_chatbot_lib.extractor import extract_json, extract_json_list, validate_schema
from groq_chatbot_lib.tools import ToolDefinition, ToolCall, ToolResult


class ChatbotClient:

    def __init__(self,
                 api_key: str,
                 model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self._client = Groq(api_key=api_key)
        self._history = []
        self._memory_limit = None

    # ---- GROUP 1: Core chat methods ----

    def set_system_prompt(self, prompt: str) -> None:
        self._history = [{"role": "system", "content": prompt}]

    def ask(self, user_message: str) -> str:
        self._history.append({"role": "user", "content": user_message})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=self._history
        )

        reply = response.choices[0].message.content
        self._history.append({"role": "assistant", "content": reply})
        self._apply_memory_limit()
        return reply

    def quick_ask(self, user_message: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

    def get_history(self) -> list:
        return self._history

    def reset(self) -> None:
        self._history = []

    def _apply_memory_limit(self) -> None:
        if self._memory_limit is None:
            return
        system_messages = [m for m in self._history if m["role"] == "system"]
        conversation = [m for m in self._history if m["role"] != "system"]
        if len(conversation) > self._memory_limit:
            conversation = conversation[-self._memory_limit:]
        self._history = system_messages + conversation

    # ---- GROUP 2: Structured output methods ----

    def ask_for_json(self, prompt: str, system_prompt: str = "") -> Optional[dict]:
        raw_response = self.quick_ask(prompt, system_prompt=system_prompt)
        return extract_json(raw_response)

    def ask_for_json_list(self, prompt: str, system_prompt: str = "") -> list[dict]:
        raw_response = self.quick_ask(prompt, system_prompt=system_prompt)
        return extract_json_list(raw_response)

    def ask_with_schema(self, prompt: str, required_keys: list[str], system_prompt: str = "") -> Optional[dict]:
        data = self.ask_for_json(prompt, system_prompt=system_prompt)
        if data is None:
            return None
        if not validate_schema(data, required_keys):
            return None
        return data

    # ---- GROUP 3: Context & memory control ----

    def set_memory_limit(self, limit: int) -> None:
        if limit < 1:
            raise ValueError("Memory limit must be at least 1")
        self._memory_limit = limit
        self._apply_memory_limit()

    def get_recent_history(self, n: int) -> list:
        if n < 1:
            raise ValueError("n must be at least 1")
        conversation = [m for m in self._history if m["role"] != "system"]
        return conversation[-n:]

    def inject_context(self, role: str, content: str) -> None:
        allowed_roles = {"user", "assistant", "system"}
        if role not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        if not content or not content.strip():
            raise ValueError("content cannot be empty")
        self._history.append({"role": role, "content": content.strip()})

    def trim_history(self, keep_last: int) -> None:
        if keep_last < 1:
            raise ValueError("keep_last must be at least 1")
        system_messages = [m for m in self._history if m["role"] == "system"]
        conversation = [m for m in self._history if m["role"] != "system"]
        self._history = system_messages + conversation[-keep_last:]

    def get_memory_limit(self) -> Optional[int]:
        return self._memory_limit

    def remove_memory_limit(self) -> None:
        self._memory_limit = None

    def count_turns(self) -> int:
        return len([m for m in self._history if m["role"] != "system"])

    def has_system_prompt(self) -> bool:
        return any(m["role"] == "system" for m in self._history)

    # ---- GROUP 4: Tool calling ----

    async def ask_with_tools(
        self,
        user_message: str,
        tools: list[ToolDefinition],
        executor: Callable[[ToolCall], Awaitable[ToolResult]]
    ) -> str:

        # STEP 1 — append user message, call Groq with tool definitions
        self._history.append({"role": "user", "content": user_message})

        groq_tools = [t.to_groq_format() for t in tools]

        response = await asyncio.to_thread(
            self._client.chat.completions.create,
            model=self.model,
            messages=self._history,
            tools=groq_tools,
            tool_choice="auto"
        )

        # STEP 2 — did AI reply with text or request a tool?
        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason != "tool_calls" or not message.tool_calls:
            reply = message.content or ""
            self._history.append({"role": "assistant", "content": reply})
            self._apply_memory_limit()
            return reply

        # STEP 3 — AI requested tools, run each one
        assistant_message = {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        }
        self._history.append(assistant_message)

        for raw_call in message.tool_calls:
            try:
                arguments = json.loads(raw_call.function.arguments)
            except json.JSONDecodeError:
                arguments = {}

            tool_call = ToolCall(
                id=raw_call.id,
                name=raw_call.function.name,
                arguments=arguments
            )

            try:
                result = await executor(tool_call)
            except Exception as e:
                result = ToolResult(
                    tool_call_id=tool_call.id,
                    content=f"Tool execution failed: {str(e)}",
                    is_error=True
                )

            self._history.append(result.to_groq_message())

        # STEP 4 — send results back, get final reply
        final_response = await asyncio.to_thread(
            self._client.chat.completions.create,
            model=self.model,
            messages=self._history
        )

        final_reply = final_response.choices[0].message.content or ""
        self._history.append({"role": "assistant", "content": final_reply})
        self._apply_memory_limit()
        return final_reply