replacements = {
	"$HOME": "postgresql://user:pass@localhost:5432/mydb",
	"ENV_API_TIMEOUT": "30",
	"ENV_DEBUG_MODE": "False",
	"ENV_APP_ENV": "production"
}
def process_document_env_vars(file_path: str, replacements) -> None:
	"""
	Replaces a predefined list of environment variables/strings in a document 
	with their processed values, taking only the file path as an argument.
	"""
	try:
		# Read the document content safely
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.read()

		# Iterate through the dictionary and replace all instances
		for target, replacement in replacements.items():
			content = content.replace(target, str(replacement))

		# Write the modified content back to the file
		with open(file_path, 'w', encoding='utf-8') as file:
			file.write(content)

		print(f"Successfully updated document: {file_path}")

	except FileNotFoundError:
		print(f"Error: The file at '{file_path}' was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")

# Example usage:
# process_document_env_vars("config.template.txt", replacements)