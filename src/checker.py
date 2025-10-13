## File 3: `src/checker.py`

'''python'''
"""
Password strength checker implementation.
"""

import re
import math
from typing import List, Tuple
from .models import PasswordAnalysis, StrengthLevel


class PasswordStrengthChecker:
    """
    A comprehensive password strength checker that analyzes passwords
    based on multiple security criteria.
    """
    
    # Common weak passwords and patterns
    COMMON_PASSWORDS = [
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321',
        'admin', 'welcome', 'login', 'password1', 'qwerty123'
    ]
    
    COMMON_PATTERNS = ['123', 'abc', 'qwe', '111', '000', 'aaa']
    
    KEYBOARD_PATTERNS = [
        'qwerty', 'asdfgh', 'zxcvbn', '1qaz', '2wsx',
        'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
    ]
    
    def __init__(self):
        """Initialize the password strength checker."""
        self.min_length = 8
        self.recommended_length = 12
        self.strong_length = 16
    
    def check_strength(self, password: str) -> PasswordAnalysis:
        """
        Analyze password strength and return comprehensive results.
        
        Args:
            password: The password to analyze
            
        Returns:
            PasswordAnalysis object containing detailed analysis
        """
        if not password:
            return PasswordAnalysis(
                password="",
                strength=StrengthLevel.VERY_WEAK,
                score=0,
                entropy=0.0,
                feedback=["Password cannot be empty"],
                time_to_crack="Instant"
            )
        
        score = 0
        feedback = []
        
        # Length analysis
        length_score, length_feedback = self._check_length(password)
        score += length_score
        feedback.extend(length_feedback)
        
        # Character variety analysis
        variety_score, variety_feedback = self._check_character_variety(password)
        score += variety_score
        feedback.extend(variety_feedback)
        
        # Pattern and common password detection
        pattern_penalty, pattern_feedback = self._check_patterns(password)
        score += pattern_penalty
        feedback.extend(pattern_feedback)
        
        # Sequential and repeated character detection
        sequence_penalty, sequence_feedback = self._check_sequences(password)
        score += sequence_penalty
        feedback.extend(sequence_feedback)
        
        # Calculate entropy
        entropy = self._calculate_entropy(password)
        
        # Determine strength level
        strength = self._determine_strength(score, entropy)
        
        # Estimate time to crack
        time_to_crack = self._estimate_crack_time(entropy)
        
        return PasswordAnalysis(
            password=password,
            strength=strength,
            score=max(0, score),
            entropy=entropy,
            feedback=feedback if feedback else ["Password meets security requirements"],
            time_to_crack=time_to_crack
        )
    
    def _check_length(self, password: str) -> Tuple[int, List[str]]:
        """Check password length and assign score."""
        length = len(password)
        feedback = []
        score = 0
        
        if length < self.min_length:
            feedback.append(f"Password too short. Use at least {self.min_length} characters")
            score -= 2
        elif length >= self.strong_length:
            score += 3
        elif length >= self.recommended_length:
            score += 2
        else:
            score += 1
            feedback.append(f"Consider using at least {self.recommended_length} characters")
        
        return score, feedback
    
    def _check_character_variety(self, password: str) -> Tuple[int, List[str]]:
        """Check for character variety (uppercase, lowercase, digits, symbols)."""
        feedback = []
        score = 0
        
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
        
        if has_lower:
            score += 1
        else:
            feedback.append("Add lowercase letters (a-z)")
        
        if has_upper:
            score += 1
        else:
            feedback.append("Add uppercase letters (A-Z)")
        
        if has_digit:
            score += 1
        else:
            feedback.append("Add numbers (0-9)")
        
        if has_symbol:
            score += 2
        else:
            feedback.append("Add special characters (!@#$%^&*)")
        
        return score, feedback
    
    def _check_patterns(self, password: str) -> Tuple[int, List[str]]:
        """Check for common passwords and patterns."""
        feedback = []
        penalty = 0
        
        lower_pwd = password.lower()
        
        # Check against common passwords
        if lower_pwd in self.COMMON_PASSWORDS:
            feedback.append("This is a commonly used password - avoid it")
            penalty -= 5
        
        # Check for common patterns
        for pattern in self.COMMON_PATTERNS:
            if pattern in lower_pwd:
                feedback.append(f"Avoid common patterns like '{pattern}'")
                penalty -= 1
                break
        
        return penalty, feedback
    
    def _check_sequences(self, password: str) -> Tuple[int, List[str]]:
        """Check for repeated and sequential characters."""
        feedback = []
        penalty = 0
        
        # Check for repeated characters (3+ same characters in a row)
        if re.search(r'(.)\1{2,}', password):
            feedback.append("Avoid repeated characters (e.g., 'aaa', '111')")
            penalty -= 1
        
        # Check for keyboard sequences
        lower_pwd = password.lower()
        for pattern in self.KEYBOARD_PATTERNS:
            if pattern in lower_pwd:
                feedback.append("Avoid keyboard patterns")
                penalty -= 1
                break
        
        return penalty, feedback
    
    def _calculate_entropy(self, password: str) -> float:
        """
        Calculate password entropy in bits.
        Entropy = log2(charset_size^length)
        """
        charset_size = 0
        
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            charset_size += 32  # Approximate number of common symbols
        
        if charset_size == 0:
            return 0.0
        
        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)
    
    def _determine_strength(self, score: int, entropy: float) -> StrengthLevel:
        """Determine overall password strength based on score and entropy."""
        if score <= 0 or entropy < 28:
            return StrengthLevel.VERY_WEAK
        elif score <= 2 or entropy < 36:
            return StrengthLevel.WEAK
        elif score <= 4 or entropy < 50:
            return StrengthLevel.FAIR
        elif score <= 6 or entropy < 60:
            return StrengthLevel.GOOD
        elif score <= 8 or entropy < 70:
            return StrengthLevel.STRONG
        else:
            return StrengthLevel.VERY_STRONG
    
    def _estimate_crack_time(self, entropy: float) -> str:
        """
        Estimate time to crack password using brute force.
        Assumes 1 billion guesses per second.
        """
        attempts = 2 ** entropy
        guesses_per_second = 1e9
        seconds = attempts / guesses_per_second
        
        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds / 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds / 3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds / 86400)} days"
        elif seconds < 31536000 * 100:
            return f"{int(seconds / 31536000)} years"
        else:
            return "Centuries"
