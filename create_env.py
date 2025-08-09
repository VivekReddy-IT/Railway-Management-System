import os

# The API key
api_key = "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"

# Create .env file with UTF-8 encoding
with open('.env', 'w', encoding='utf-8') as f:
    f.write(f"GROQ_API_KEY={api_key}")

print("Created .env file successfully!") 