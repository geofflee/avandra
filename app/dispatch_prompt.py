from typing import Awaitable, Callable
from backends.anthropic import AnthropicClient
import tools


async def _get_emojis(send_reply: Callable[[str], Awaitable[None]]) -> None:
    """Returns a string of all emojis for the dice roller."""
    output = (
        "".join(f"{tools.roll_dice.get_emoji(4, i)}" for i in range(1, 5))
        + "".join(f"{tools.roll_dice.get_emoji(6, i)}" for i in range(1, 7))
        + f"{tools.roll_dice.get_emoji(19, 1)}"
        + "".join(f"{tools.roll_dice.get_emoji(20, i)}" for i in range(1, 21))
    )
    await send_reply(output)


async def _ask_claude(
    anthropic_client: AnthropicClient,
    character_name: str,
    user_prompt: str,
    handle_tool: Callable[[str, dict | str], Awaitable[str]],
    send_reply: Callable[[str], Awaitable[None]],
) -> None:
    """Asks Claude to handle a user prompt."""
    tool_list = [
        tools.character_sheet.tool_json_schema(),
        tools.roll_dice.tool_json_schema(),
    ]
    # print(to_json(tool_list, indent=2).decode())
    system_prompt = [
        {
            "type": "text",
            "text": (
                "You are the goddess Avandra, patron deity of luck and adventure. "
                "You help run a D&D 5e campaign by reading a character sheet and "
                "rolling dice."  # Speak in a fateful voice."
                "\n\n"
                "Before rolling dice, explain the relevant character stat and what "
                "dice you will roll, but don't describe the outcomes."
            ),
        },
    ]
    if character_prompt := tools.character_sheet.system_prompt(character_name):
        character_prompt["cache_control"] = {"type": "ephemeral"}
        system_prompt.append(character_prompt)
    await anthropic_client.call(
        system_prompt=system_prompt,
        tools=tool_list,
        handle_tool=handle_tool,
        user_prompt=user_prompt,
        send_reply=send_reply,
    )


async def handle_prompt(
    anthropic_client: AnthropicClient,
    character_name: str,
    user_prompt: str,
    handle_tool: Callable[[str, dict | str], Awaitable[str]],
    send_reply: Callable[[str], Awaitable[None]],
) -> None:
    """A callback that handles a user prompt."""
    match user_prompt:
        case "emojis":
            await _get_emojis(send_reply)
        case _:
            await _ask_claude(
                anthropic_client,
                character_name,
                user_prompt,
                handle_tool,
                send_reply,
            )
