from __future__ import annotations
import asyncio
import discord
from typing import Awaitable, Callable

def get_character_name(user_name: str) -> str:
	"""Get the character's name from their Discord user name."""
	match user_name:
		case "archangeloflife":
			return "Zauber Stab"
		case "bfahy":
			return "Vesper"
		case "geofflee":
			return "Hoglat"
		case "onethree111":
			return "Alistair Darrow"
		case _:
			return ""

class DiscordClient(discord.Client):
	"""Discord client for the bot.
	
	See https://discordpy.readthedocs.io/en/stable/api.html for more information.
	"""

	HandlePromptFn = Callable[[str, str, Callable[[str], Awaitable[None]]], Awaitable[None]]

	def __init__(self, handle_prompt: DiscordClient.HandlePromptFn):
		"""Initializes the Discord client.
		
		Args:
			handle_prompt: A callback that takes a character name and a prompt,
				and returns a response.
		"""
		intents = discord.Intents.default()
		intents.message_content = True
		super().__init__(intents=intents)
		self._handle_prompt = handle_prompt

	async def on_ready(self):
		print(f"Logged in as {self.user}")

	async def on_message(self, message):
		is_me = message.author == self.user
		is_trigger = (message.content.startswith("!")
			or message.channel.type == discord.ChannelType.private
			or self.user.mentioned_in(message))
		
		if is_trigger or is_me:
			print(f"{message.author.display_name}: {message.content}")

		if is_trigger and not is_me:
			character_name = get_character_name(message.author.name)
			user_prompt = message.content[1:] if message.content.startswith("!") else message.content

			async def send_reply(output: str):
				await message.channel.send(f'{message.author.mention} {output}')

			async with message.channel.typing():
				await self._handle_prompt(character_name, user_prompt, send_reply)

	_handle_prompt: DiscordClient.HandlePromptFn
