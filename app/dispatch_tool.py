import tools
from typing import Awaitable, Callable


async def handle_tool(
    tool_name: str,
    input: dict | str,
    send_reply: Callable[[str], Awaitable[None]],
) -> str:
    """Run a tool."""
    match tool_name:
        case "get_character_sheet":
            return await tools.character_sheet.run(input, send_reply)
        case "roll_dice":
            return await tools.roll_dice.run(input, send_reply)
        case _:
            await send_reply(f"Unknown tool: {tool_name}")
            return f"Unknown tool: {tool_name}"
