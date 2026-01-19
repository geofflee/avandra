from typing import Awaitable, Callable
import tools


async def handle_tool(
    tool_name: str,
    tool_input: dict | str,
    send_reply: Callable[[str], Awaitable[None]],
) -> str:
    """Run a tool."""
    match tool_name:
        case "get_character_sheet":
            return await tools.character_sheet.run(tool_input, send_reply)
        case "roll_dice":
            return await tools.roll_dice.run(tool_input, send_reply)
        case _:
            await send_reply(f"Unknown tool: {tool_name}")
            return f"Unknown tool: {tool_name}"
