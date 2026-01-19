import os
from backends import gcp


def discord_token() -> str:
    """Returns the Discord token, checking environment variables first.

    Returns:
      str: The Discord token from environment variable DISCORD_TOKEN if set,
        otherwise from GCP secret manager.
    """
    if token := os.getenv("DISCORD_TOKEN"):
        return token
    return gcp.get_discord_token()


def anthropic_key() -> str:
    """Returns the Anthropic API key, checking environment variables first.

    Returns:
      str: The Anthropic API key from environment variable ANTHROPIC_KEY if set,
        otherwise from GCP secret manager.
    """
    if key := os.getenv("ANTHROPIC_KEY"):
        return key
    return gcp.get_anthropic_key()
