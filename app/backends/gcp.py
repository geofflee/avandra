import google_crc32c
from google.cloud import secretmanager

PROJECT_ID = "915826390368"

def memoize(func):
	"""Decorator to memoize a function's return value."""
	cache = {}
	def wrapper(*args, **kwargs):
		if func not in cache:
			cache[func] = func(*args, **kwargs)
		return cache[func]
	return wrapper

@memoize
def client() -> secretmanager.SecretManagerServiceClient:
	"""Returns the Secret Manager client."""
	return secretmanager.SecretManagerServiceClient()

def _get_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
	"""
	Fetches a secret from Google Cloud Secret Manager and validates its integrity.
	
	Args:
		project_id: The GCP project ID
		secret_id: The ID of the secret to fetch
		version_id: The version of the secret to fetch (defaults to "latest")
	
	Returns:
		The secret value as a string
	
	Raises:
		Exception if the secret cannot be fetched or if CRC32C validation fails
	"""
	# Build the resource name of the secret version
	name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
	
	# Access the secret version using the shared client
	response = client().access_secret_version(request={"name": name})
	
	# Verify payload checksum
	crc32c = google_crc32c.Checksum()
	crc32c.update(response.payload.data)
	if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
		raise Exception("Data corruption detected.")
	
	# Return the secret payload
	return response.payload.data.decode("UTF-8")

@memoize
def get_anthropic_key() -> str:
	"""Fetches the Anthropic API key from Google Cloud Secret Manager.
	
	The key is cached after the first fetch to minimize API calls to Secret Manager.
	
	Returns:
		str: The Anthropic API key
	"""
	return _get_secret(PROJECT_ID, "anthropic-key")

@memoize
def get_discord_token() -> str:
	"""Fetches the Discord token from Google Cloud Secret Manager.
	
	Returns:
		str: The Discord bot token
	"""
	return _get_secret(PROJECT_ID, "discord-token")

@memoize
def get_postgres_password() -> str:
	"""Fetches the Postgres password from Google Cloud Secret Manager.
	
	Returns:
		str: The Postgres password
	"""
	return _get_secret(PROJECT_ID, "porygon-password")
