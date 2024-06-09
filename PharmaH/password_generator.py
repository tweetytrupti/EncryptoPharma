import secrets
import string

def generate_password(length=12):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")
    
    # Character sets
    all_characters = string.ascii_letters + string.digits + string.punctuation
    
    # Ensure at least one character from each required set
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    
    # Fill the rest of the password length with random characters
    password += [secrets.choice(all_characters) for _ in range(length - 4)]
    
    # Shuffle to ensure randomness
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


