from typing import Annotated, Awaitable, Callable
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import to_json


class AbilityScore(BaseModel):
    """A character's ability score."""

    score: Annotated[
        int,
        Field(
            description="The score of the ability.",
            ge=1,
            le=30,
            default=10,
        ),
    ]
    proficient: Annotated[
        bool,
        Field(
            description="Whether the character is proficient with the ability.",
            default=False,
        ),
    ]


class CharacterClass(BaseModel):
    """A character's class."""

    class_name: Annotated[
        str,
        Field(
            description="The name of the character's class.",
            min_length=1,
        ),
    ]
    level: Annotated[
        int,
        Field(
            description="The level of the character's class.",
            ge=1,
            le=20,
        ),
    ]


class CharacterSheet(BaseModel):
    """D&D 5e character sheet."""

    model_config = ConfigDict(strict=True)

    name: Annotated[
        str,
        Field(
            description="The name of the character.",
            min_length=1,
        ),
    ]
    race: Annotated[
        str,
        Field(
            description="The race of the character.",
            min_length=1,
        ),
    ]
    gender: Annotated[
        str,
        Field(
            description="The gender of the character.",
            min_length=1,
        ),
    ]
    total_character_level: Annotated[
        int,
        Field(
            description="The level of the character.",
            ge=1,
            le=30,
            default=1,
        ),
    ]
    classes: Annotated[
        list[CharacterClass],
        Field(
            description="The character's classes.",
        ),
    ]
    strength: Annotated[
        AbilityScore,
        Field(
            description="The character's Strength score.",
        ),
    ]
    dexterity: Annotated[
        AbilityScore,
        Field(
            description="The character's Dexterity score.",
        ),
    ]
    constitution: Annotated[
        AbilityScore,
        Field(
            description="The character's Constitution score.",
        ),
    ]
    intelligence: Annotated[
        AbilityScore,
        Field(
            description="The character's Intelligence score.",
        ),
    ]
    wisdom: Annotated[
        AbilityScore,
        Field(
            description="The character's Wisdom score.",
        ),
    ]
    charisma: Annotated[
        AbilityScore,
        Field(
            description="The character's Charisma score.",
        ),
    ]
    skill_proficiencies: Annotated[
        list[str],
        Field(
            description="List of the character's skill proficiencies.",
            default_factory=list,
        ),
    ]
    weapon_proficiencies: Annotated[
        list[str],
        Field(
            description="List of the character's weapon proficiencies.",
            default_factory=list,
        ),
    ]
    other: Annotated[
        list[str],
        Field(
            description="List of the character's other attributes.",
            default_factory=list,
        ),
    ]


# TODO: Move this to a database.
sheets = {
    "Alistair Darrow": CharacterSheet(
        name="Alistair Darrow",
        race="Human",
        gender="Male",
        total_character_level=3,
        classes=[
            CharacterClass(class_name="Wizard", level=3),
        ],
        strength=AbilityScore(score=9),
        dexterity=AbilityScore(score=13),
        constitution=AbilityScore(score=11),
        intelligence=AbilityScore(score=16, proficient=True),
        wisdom=AbilityScore(score=14, proficient=True),
        charisma=AbilityScore(score=15),
        skill_proficiencies=[
            "Arcana",
            "Athletics",
            "Insight",
            "Investigation",
        ],
        weapon_proficiencies=[
            "Crossbow",
            "Light Dagger",
            "Quarterstaff",
            "Sling",
        ],
    ),
    "Hoglat": CharacterSheet(
        name="Hoglat",
        race="Human",
        gender="Male",
        total_character_level=3,
        classes=[
            CharacterClass(class_name="Cleric", level=3),
        ],
        strength=AbilityScore(score=16, proficient=True),
        dexterity=AbilityScore(score=12),
        constitution=AbilityScore(score=15),
        intelligence=AbilityScore(score=8),
        wisdom=AbilityScore(score=14, proficient=True),
        charisma=AbilityScore(score=10),
        skill_proficiencies=[
            "Acrobatics",
            "Athletics (Expertise)",
            "Insight",
            "Intimidation",
            "Medicine",
        ],
        weapon_proficiencies=[
            "Maul",
            "Simple Weapons",
            "Heavy Weapons",
        ],
    ),
    "Vesper": CharacterSheet(
        name="Vesper",
        race="Stout Halfling",
        gender="Male",
        total_character_level=3,
        classes=[
            CharacterClass(class_name="Bard", level=3),
        ],
        strength=AbilityScore(score=10),
        dexterity=AbilityScore(score=15, proficient=True),
        constitution=AbilityScore(score=13),
        intelligence=AbilityScore(score=14),
        wisdom=AbilityScore(score=8),
        charisma=AbilityScore(score=15, proficient=True),
        skill_proficiencies=[
            "Acrobatics",
            "Deception",
            "Insight (Expertise)",
            "Performance (Expertise)",
            "Persuasion",
        ],
        weapon_proficiencies=[
            "Crossbow",
            "Hand",
            "Longsword",
            "Rapier",
            "Shortsword",
            "Simple Weapons",
        ],
        other=[
            "Advantage against being frightened",
            "Advantage against poison",
            "Jack of All Trades",
        ],
    ),
    "Zauber Stab": CharacterSheet(
        name="Zauber Stab",
        race="Half-Orc",
        gender="Male",
        total_character_level=3,
        classes=[
            CharacterClass(class_name="Barbarian", level=3),
        ],
        strength=AbilityScore(score=16, proficient=True),
        dexterity=AbilityScore(score=13),
        constitution=AbilityScore(score=16, proficient=True),
        intelligence=AbilityScore(score=10),
        wisdom=AbilityScore(score=12),
        charisma=AbilityScore(score=8),
        skill_proficiencies=[
            "Athletics",
            "Intimidation",
            "Survival",
        ],
        weapon_proficiencies=[
            "Martial Weapons",
            "Simple Weapons",
        ],
        other=[
            "Advantage on DEX against effects that you can see while not blinded, deafened, or incapacitated.",
            "+1 on all Arcana checks.",
        ],
    ),
}


class GetCharacterSheetInput(BaseModel):
    model_config = ConfigDict(strict=True)

    character_name: Annotated[
        str,
        Field(
            description="Name of the character to get the character sheet for.",
            enum=list(sheets.keys()),
        ),
    ]


def get_character_sheet(input: GetCharacterSheetInput) -> str:
    """Get a character sheet."""
    if input.character_name not in sheets:
        raise ValueError(f"Character {input.character_name} not found.")
    else:
        return sheets[input.character_name].model_dump_json(indent=2)


def system_prompt(character_name: str) -> dict | None:
    """System prompt for the character sheet tool."""
    party_members = to_json(list(sheets.keys())).decode()
    if character_name not in sheets:
        return {
            "type": "text",
            "text": (f"The party members are: {party_members}"),
        }
    else:
        sheet = sheets[character_name].model_dump_json(indent=2)
        return {
            "type": "text",
            "text": (
                f"The party members are: {party_members}\n\n"
                f"Here is the player's character sheet:\n{sheet}"
            ),
        }


def tool_json_schema() -> dict:
    """Returns the JSON schema for the roll tool."""
    return {
        "name": "get_character_sheet",
        "description": get_character_sheet.__doc__,
        "input_schema": GetCharacterSheetInput.model_json_schema(),
    }


async def run(input: dict | str, send_reply: Callable[[str], Awaitable[None]]) -> str:
    """Run the get_character_sheet tool."""
    if isinstance(input, str):
        inputs = GetCharacterSheetInput.model_validate_json(input)
    else:
        inputs = GetCharacterSheetInput.model_validate(input)
    return get_character_sheet(inputs)
