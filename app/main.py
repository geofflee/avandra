"""Main entry point for the Avandra Discord bot."""

import argparse
from backends.anthropic import AnthropicClient
from backends.discord import DiscordClient
import credentials
import dispatch_prompt
import dispatch_tool

def make_handle_prompt(
		anthropic_client: AnthropicClient) -> DiscordClient.HandlePromptFn:
	"""Returns a callback that handles a user prompt."""
	return lambda character_name, user_prompt, handle_output: dispatch_prompt.handle_prompt(
		anthropic_client,
		character_name,
		user_prompt,
		dispatch_tool.handle_tool,
		handle_output,
	)

def run_interactive(anthropic_client: AnthropicClient, character_name: str):
	"""Run the job in interactive mode."""
	handle_prompt = make_handle_prompt(anthropic_client)
	handle_output = lambda output: print(output + "\n")
	while True:
		try:
			user_prompt = input("> ")
			if user_prompt == "exit":
				break
			handle_prompt(character_name, user_prompt, handle_output)
		except EOFError:
			break
		except KeyboardInterrupt:
			break

def run_discord(anthropic_client: AnthropicClient):
	"""Run the job in Discord mode."""
	client = DiscordClient(make_handle_prompt(anthropic_client))
	client.run(credentials.discord_token())

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run the Avandra Discord bot")
	parser.add_argument("--interactive", action="store_true", help="Run in interactive mode instead of Discord")
	parser.add_argument("--name", type=str, help="The name of the character in interactive mode", default="Hoglat")
	args = parser.parse_args()

	anthropic_client = AnthropicClient(credentials.anthropic_key())

	if args.interactive:
		run_interactive(anthropic_client, args.name)
	else:
		run_discord(anthropic_client)
