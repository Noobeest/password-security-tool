"""
Data models for password analysis.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List




class StrengthLevel(Enum):
    """Enumeration for password strength levels."""
    VERY_WEAK = 0
    WEAK = 1
    FAIR = 2
    GOOD = 3
    STRONG = 4
    VERY_STRONG = 5


@dataclass
class PasswordAnalysis:
    """Data class for password analysis results."""
    password: str
    strength: StrengthLevel
    score: int
    entropy: float
    feedback: List[str]
    time_to_crack: str
    
    def __str__(self) -> str:
        """String representation of analysis."""
        return (
            f"Strength: {self.strength.name}\n"
            f"Score: {self.score}/10\n"
            f"Entropy: {self.entropy} bits\n"
            f"Time to crack: {self.time_to_crack}"
        )
