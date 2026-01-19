from typing import Annotated, Awaitable, Callable
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import to_json
import random


class DiceRollInput(BaseModel):
    model_config = ConfigDict(strict=True)

    sides: Annotated[
        int,
        Field(
            description="The number of sides on the die.",
            ge=1,
        ),
    ]
    times: Annotated[
        int,
        Field(
            description="Optional. Number of times to roll the die.",
            default=1,
            ge=1,
        ),
    ]
    # modifier: Annotated[int, Field(
    # 	description="The roll modifier.",
    # )]
    # mode: Annotated[str, Field(
    # 	description="Optional. Whether to roll with advantage or disadvantage.",
    # 	default="normal",
    # 	enum=["normal", "advantage", "disadvantage"],
    # )]

    def stringify(self) -> str:
        """Prints the input object."""
        return f"{self.times}d{self.sides}"
        # modifier_sign = "+" if self.modifier >= 0 else ""
        # modifier = "" if self.modifier == 0 else f"{modifier_sign}{self.modifier}"
        # if self.mode == "advantage":
        # 	output = f"{self.times}d{self.sides}{modifier} advantage"
        # elif self.mode == "disadvantage":
        # 	output = f"{self.times}d{self.sides}{modifier} disadvantage"
        # else:
        # 	output = f"{self.times}d{self.sides}{modifier}"
        # return output


def get_emoji(sides: int, value: int) -> str:
    """Returns the emoji for a die of a given number of sides and value.

    If no such emoji exists, returns the value as a string.

    See: https://discord.com/developers/applications/1355649776649113950/emojis"""
    if sides > 20:
        return f"{value}"

    match sides:
        case 4:
            match value:
                case 1:
                    return "<:d4_1:1361141389756203248>"
                case 2:
                    return "<:d4_2:1361141429585444976>"
                case 3:
                    return "<:d4_3:1361141445649629385>"
                case 4:
                    return "<:d4_4:1361141459910135858>"
        case 6:
            match value:
                case 1:
                    return "<:d6_1:1361146264963645520>"
                case 2:
                    return "<:d6_2:1361147339661901964>"
                case 3:
                    return "<:d6_3:1361147351624061248>"
                case 4:
                    return "<:d6_4:1361147359915937792>"
                case 5:
                    return "<:d6_5:1361147368187236412>"
                case 6:
                    return "<:d6_6:1361147376131113080>"
        case _:
            match value:
                case 1:
                    if sides == 20:
                        return "<:d20_1:1356083355460042923>"
                    else:
                        return "<:d_1:1361142075453735073>"
                case 2:
                    return "<:d20_2:1356088534494351414>"
                case 3:
                    return "<:d20_3:1356088583181697206>"
                case 4:
                    return "<:d20_4:1356089534906896424>"
                case 5:
                    return "<:d20_5:1356094275670114318>"
                case 6:
                    return "<:d20_6:1356104989075968180>"
                case 7:
                    return "<:d20_7:1356105384997158932>"
                case 8:
                    return "<:d20_8:1356106235384172564>"
                case 9:
                    return "<:d20_9:1356131184647868476>"
                case 10:
                    return "<:d20_10:1356131225592659988>"
                case 11:
                    return "<:d20_11:1356131251580440707>"
                case 12:
                    return "<:d20_12:1356131268164583424>"
                case 13:
                    return "<:d20_13:1356131281141764247>"
                case 14:
                    return "<:d20_14:1356131293594910932>"
                case 15:
                    return "<:d20_15:1356131307595370506>"
                case 16:
                    return "<:d20_16:1356131322225102878>"
                case 17:
                    return "<:d20_17:1356138165869740153>"
                case 18:
                    return "<:d20_18:1356138176569151508>"
                case 19:
                    return "<:d20_19:1356138185666854997>"
                case 20:
                    return "<:d20_20:1356138194634276981>"

    # Should never reach here
    return f"{value}"


async def roll_dice(
    input: DiceRollInput, send_reply: Callable[[str], Awaitable[None]]
) -> str:
    """Rolls dice.

    Allows the caller to specify the number of sides, the number of times to roll.
    """

    # ,
    # an optional modifier, and the mode of the roll (normal, advantage, or
    # disadvantage).
    # """
    def roll(sides: int, times: int) -> list[int]:
        return [random.randint(1, sides) for _ in range(times)]

    def to_emojis(rolls: list[int]) -> str:
        return " ".join(f"{get_emoji(input.sides, roll)}" for roll in rolls)

    if input.sides < 1:
        return "Number of sides must be at least 1."

    # if input.times == 1 and input.mode == "normal" and input.modifier == 0:
    # 	breakdown = get_emoji(input.sides, roll(input.sides, 1)[0])
    # 	return f"{input.stringify()} -> {breakdown}"

    rolls = roll(input.sides, input.times)
    await send_reply(f"{input.stringify()} -> {to_emojis(rolls)}")
    return to_json(
        {
            "rolls": rolls,
        }
    ).decode()

    if input.mode == "normal":
        rolls = roll(input.sides, input.times)
        breakdown = to_emojis(rolls)
        total = sum(rolls) + input.modifier
        tool_result = to_json(
            {
                "rolls": rolls,
                "modifier": input.modifier,
                "total": total,
            }
        ).decode()
    else:  # advantage or disadvantage
        roll_1 = roll(input.sides, input.times)
        roll_2 = roll(input.sides, input.times)
        breakdown_1 = to_emojis(roll_1)
        breakdown_2 = to_emojis(roll_2)
        breakdown = f"({breakdown_1} | {breakdown_2})"
        if input.mode == "advantage":
            total = max(sum(roll_1), sum(roll_2))
        else:
            total = min(sum(roll_1), sum(roll_2))
        total += input.modifier
        tool_result = to_json(
            {
                "rolls_1": roll_1,
                "rolls_2": roll_2,
                "modifier": input.modifier,
                "total": total,
            }
        ).decode()

    if input.modifier > 0:
        breakdown += f" + {input.modifier}"
    elif input.modifier < 0:
        breakdown += f" - {abs(input.modifier)}"

    await send_reply(f"{input.stringify()} -> {breakdown} -> {total}")
    return tool_result


def tool_json_schema() -> dict:
    """Returns the JSON schema for the roll tool."""
    return {
        "name": "roll_dice",
        "description": roll_dice.__doc__,
        "input_schema": DiceRollInput.model_json_schema(),
    }


async def run(input: dict | str, send_reply: Callable[[str], Awaitable[None]]) -> str:
    """Runs the roll_dice tool on a json input."""
    if isinstance(input, str):
        inputs = DiceRollInput.model_validate_json(input)
    else:
        inputs = DiceRollInput.model_validate(input)
    output = await roll_dice(inputs, send_reply)
    return output
