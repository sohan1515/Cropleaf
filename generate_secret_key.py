#!/usr/bin/env python
"""
Generate a secure Django SECRET_KEY for production use
"""
import secrets

def generate_secret_key():
    """Generate a cryptographically secure secret key"""
    return secrets.token_urlsafe(50)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Django SECRET_KEY:")
    print(secret_key)
    print("\nCopy this key to your Render environment variables as SECRET_KEY")