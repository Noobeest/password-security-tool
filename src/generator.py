## File 4: `src/generator.py`

'''python'''
"""
Secure password generator implementation.
"""

import secrets
import string
from typing import List


class PasswordGenerator:
    """
    A secure password generator using cryptographically strong random generation.
    """
    
    def __init__(self):
        """Initialize the password generator."""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Extended word list for passphrases
        self.word_list = [
            "correct", "horse", "battery", "staple", "mountain", "river",
            "ocean", "forest", "castle", "dragon", "wizard", "knight",
            "phoenix", "thunder", "crystal", "shadow", "silver", "golden",
            "mystic", "ancient", "cosmic", "digital", "quantum", "stellar",
            "cipher", "falcon", "granite", "harbor", "island", "jungle",
            "kingdom", "lunar", "nebula", "orbit", "prism", "radar",
            "summit", "tempest", "ultraviolet", "vertex", "whisper", "xenon",
            "yellow", "zenith", "alpha", "bravo", "charlie", "delta"
        ]
    
    def generate(
        self,
        length: int = 16,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True
    ) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Length of the password (minimum 8)
            use_lowercase: Include lowercase letters
            use_uppercase: Include uppercase letters
            use_digits: Include digits
            use_symbols: Include special symbols
            
        Returns:
            Generated password string
            
        Raises:
            ValueError: If length is too short or no character types selected
        """
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")
        
        # Build character set
        charset = ""
        if use_lowercase:
            charset += self.lowercase
        if use_uppercase:
            charset += self.uppercase
        if use_digits:
            charset += self.digits
        if use_symbols:
            charset += self.symbols
        
        if not charset:
            raise ValueError("At least one character type must be selected")
        
        # Generate password ensuring at least one character from each selected type
        password = []
        
        if use_lowercase:
            password.append(secrets.choice(self.lowercase))
        if use_uppercase:
            password.append(secrets.choice(self.uppercase))
        if use_digits:
            password.append(secrets.choice(self.digits))
        if use_symbols:
            password.append(secrets.choice(self.symbols))
        
        # Fill remaining length with random characters from full charset
        remaining_length = length - len(password)
        password.extend(secrets.choice(charset) for _ in range(remaining_length))
        
        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def generate_passphrase(
        self,
        word_count: int = 4,
        separator: str = "-",
        capitalize: bool = False
    ) -> str:
        """
        Generate a memorable passphrase using random words.
        
        Args:
            word_count: Number of words in the passphrase
            separator: Character to separate words
            capitalize: Whether to capitalize first letter of each word
            
        Returns:
            Generated passphrase
            
        Raises:
            ValueError: If word_count is less than 3
        """
        if word_count < 3:
            raise ValueError("Passphrase must contain at least 3 words")
        
        selected_words = [secrets.choice(self.word_list) for _ in range(word_count)]
        
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
        
        return separator.join(selected_words)
    
    def generate_pin(self, length: int = 4) -> str:
        """
        Generate a random PIN code.
        
        Args:
            length: Length of the PIN (typically 4-6)
            
        Returns:
            Generated PIN as string
        """
        return ''.join(secrets.choice(self.digits) for _ in range(length))
    
    def generate_multiple(
        self,
        count: int = 5,
        length: int = 16,
        **kwargs
    ) -> List[str]:
        """
        Generate multiple passwords at once.
        
        Args:
            count: Number of passwords to generate
            length: Length of each password
            **kwargs: Additional arguments passed to generate()
            
        Returns:
            List of generated passwords
        """
        return [self.generate(length=length, **kwargs) for _ in range(count)]
