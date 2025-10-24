import secrets
import os

# Generate a 32-byte hex secret key
SECRET_KEY = secrets.token_hex(32)

# Path to your .env file (create it if it doesn't exist)
env_path = ".env"

# Check if .env exists, create if not
if not os.path.exists(env_path):
    with open(env_path, "w") as f:
        f.write(f"SECRET_KEY={SECRET_KEY}\n")
    print(f".env file created with SECRET_KEY={SECRET_KEY}")
else:
    # Append SECRET_KEY to existing .env
    with open(env_path, "a") as f:
        f.write(f"SECRET_KEY={SECRET_KEY}\n")
    print(f"SECRET_KEY={SECRET_KEY} added to existing .env")

