import asyncio
import time
from typing import Awaitable, Callable
import anthropic
from pydantic_core import from_json
from pydantic_core import to_json


class AnthropicClient:
    """A client for interacting with the Anthropic API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=api_key)

    async def call_api(
        self, system_prompt: list[dict], tools: list[dict], messages: list[dict]
    ) -> anthropic.types.Message:
        """Calls the Anthropic API with a given prompt."""
        return await asyncio.to_thread(
            self.client.messages.create,
            # model="claude-3-7-sonnet-latest",
            # model="claude-3-5-haiku-latest",
            model="claude-4-5-haiku-latest",
            max_tokens=1024,
            tools=tools,
            tool_choice={"type": "auto"},
            system=system_prompt,
            messages=messages,
            # betas=["token-efficient-tools-2025-02-19"],
        )

    def mock_call_api(self) -> anthropic.types.Message:
        """Mock call to the Anthropic API for testing purposes."""
        return anthropic.types.Message.model_validate(from_json("""
            {
                "id": "msg_01A7qKtLUakEX4jg9LA4HbxA",
                "content": [
                    {
                        "citations": null,
                        "text": "I'll roll 2d20 with disadvantage for you.",
                        "type": "text"
                    },
                    {
                        "id": "toolu_01Met3ioxHuaVAabavjxva2s",
                        "input": {
                            "request": {
                                "sides": 20,
                                "times": 2,
                                "mode": "disadvantage"
                            }
                        },
                        "name": "roll_dice",
                        "type": "tool_use"
                    }
                ],
                "model": "claude-3-7-sonnet-20250219",
                "role": "assistant",
                "stop_reason": "tool_use",
                "stop_sequence": null,
                "type": "message",
                "usage": {
                    "cache_creation_input_tokens": 0,
                    "cache_read_input_tokens": 0,
                    "input_tokens": 619,
                    "output_tokens": 86
                }
            }"""))

    async def call(
        self,
        system_prompt: list[dict],
        tools: list[dict],
        handle_tool: Callable[[str, dict | str], Awaitable[str]],
        send_reply: Callable[[str], Awaitable[None]],
        user_prompt: str,
    ) -> None:
        """Call the Anthropic API with a given prompt.

        Args:
                system_prompt: The system prompt.
                tools: The tools to use.
                handle_tool: A function to handle tool calls, where the first argument is
                        the tool name and the second argument is a dict or json string.
                user_prompt: The user prompt.

        Returns:
                A chat reply to the user.
        """
        # print(system_prompt)
        start_time = time.time()
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                        "cache_control": {"type": "ephemeral"},
                    },
                ],
            }
        ]

        while True:
            replies: list[str] = []

            async def enqueue_reply(reply: str) -> None:
                nonlocal replies
                replies.append(reply)

            # print(to_json(messages, indent=2).decode())
            call_start_time = time.time()
            try:
                message = await self.call_api(system_prompt, tools, messages)
            except Exception as e:
                replies.append(f"Error: {e}")
                # await send_reply(f"Error: {e}")
                break
            finally:
                call_latency = time.time() - call_start_time
                print(f"API call latency: {call_latency:.2f}s")

            print(message.to_json())
            messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                }
            )

            tool_results: list[dict] = []
            for content in message.content:
                match content.type:
                    case "text":
                        replies.append(content.text)
                        # await send_reply(content.text)
                    case "tool_use":
                        try:
                            tool_result = await handle_tool(
                                content.name, content.input, enqueue_reply
                            )
                            tool_results.append(
                                {
                                    "type": "tool_result",
                                    "tool_use_id": content.id,
                                    "content": tool_result,
                                }
                            )
                        except Exception as e:
                            replies.append(f"Error: {e}")
                            # await send_reply(f"Error: {e}")
                    case _:
                        replies.append(f"Unknown content type: {content.type}")
                        # await send_reply(f"Unknown content type: {content.type}")

            if len(tool_results) > 0:
                messages.append(
                    {
                        "role": "user",
                        "content": tool_results,
                    }
                )

            if len(replies) > 0:
                await send_reply("\n".join(replies))

            if message.stop_reason != "tool_use":
                break

        latency = time.time() - start_time
        print(f"Total latency: {latency:.2f}s")


class MockAnthropicClient(AnthropicClient):
    """A mock Anthropic client for testing purposes."""

    def call_api(
        self, system_prompt: str, tools: list[dict], user_prompt: str
    ) -> anthropic.types.Message:
        """Mock call to the Anthropic API for testing purposes."""
        return self.mock_call_api()
