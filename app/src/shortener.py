"""Short code generation logic."""
import random
import string


def generate_short_code(length: int = 6) -> str:
    """
    Generate a random short code.
    
    Args:
        length: Length of the short code (default: 6)
        
    Returns:
        Random alphanumeric string
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

