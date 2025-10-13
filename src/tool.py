## File 5: `src/tool.py`

'''python'''
"""
Main password security tool interface.
"""

from .checker import PasswordStrengthChecker
from .generator import PasswordGenerator
from .models import PasswordAnalysis


class PasswordSecurityTool:
    """
    Main class integrating password checking and generation functionality.
    """
    
    def __init__(self):
        """Initialize the password security tool."""
        self.checker = PasswordStrengthChecker()
        self.generator = PasswordGenerator()
    
    def analyze_password(self, password: str, display: bool = True) -> PasswordAnalysis:
        """
        Analyze password strength.
        
        Args:
            password: Password to analyze
            display: Whether to print the analysis
            
        Returns:
            PasswordAnalysis object
        """
        analysis = self.checker.check_strength(password)
        
        if display:
            self._display_analysis(analysis)
        
        return analysis
    
    def _display_analysis(self, analysis: PasswordAnalysis) -> None:
        """Display password analysis in formatted output."""
        print("\n" + "=" * 60)
        print("PASSWORD ANALYSIS REPORT")
        print("=" * 60)
        print(f"Strength Level: {analysis.strength.name}")
        print(f"Security Score: {analysis.score}/10")
        print(f"Entropy: {analysis.entropy} bits")
        print(f"Estimated Time to Crack: {analysis.time_to_crack}")
        print("\nFeedback:")
        for item in analysis.feedback:
            print(f"  • {item}")
        print("=" * 60 + "\n")
    
    def generate_password_interactive(self) -> str:
        """
        Interactive password generation with user input.
        
        Returns:
            Generated password
        """
        print("\n" + "=" * 60)
        print("PASSWORD GENERATOR")
        print("=" * 60)
        
        try:
            length = int(input("Password length (8-32, default 16): ") or "16")
            length = max(8, min(32, length))
            
            use_lowercase = input("Include lowercase? (Y/n): ").lower() != 'n'
            use_uppercase = input("Include uppercase? (Y/n): ").lower() != 'n'
            use_digits = input("Include digits? (Y/n): ").lower() != 'n'
            use_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
            
            password = self.generator.generate(
                length=length,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_symbols=use_symbols
            )
            
            print(f"\nGenerated Password: {password}")
            
            # Automatically analyze the generated password
            self.analyze_password(password)
            
            return password
            
        except ValueError as e:
            print(f"\nError: {e}")
            return ""
    
    def display_menu(self) -> None:
        """Display main menu and handle user interaction."""
        while True:
            print("\n" + "=" * 60)
            print("PASSWORD SECURITY TOOL")
            print("=" * 60)
            print("1. Check Password Strength")
            print("2. Generate Secure Password")
            print("3. Generate Passphrase")
            print("4. Generate Multiple Passwords")
            print("5. Security Tips")
            print("6. Exit")
            print("=" * 60)
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                password = input("\nEnter password to check: ")
                self.analyze_password(password)
            
            elif choice == '2':
                self.generate_password_interactive()
            
            elif choice == '3':
                word_count = int(input("Number of words (3-6, default 4): ") or "4")
                capitalize = input("Capitalize words? (y/N): ").lower() == 'y'
                passphrase = self.generator.generate_passphrase(
                    word_count=word_count,
                    capitalize=capitalize
                )
                print(f"\nGenerated Passphrase: {passphrase}")
                self.analyze_password(passphrase)
            
            elif choice == '4':
                count = int(input("How many passwords? (default 5): ") or "5")
                length = int(input("Password length? (default 16): ") or "16")
                passwords = self.generator.generate_multiple(count=count, length=length)
                print(f"\nGenerated {count} Passwords:")
                for i, pwd in enumerate(passwords, 1):
                    print(f"  {i}. {pwd}")
            
            elif choice == '5':
                self.display_security_tips()
            
            elif choice == '6':
                print("\nThank you for using Password Security Tool!")
                break
            
            else:
                print("\nInvalid choice. Please try again.")
    
    @staticmethod
    def display_security_tips() -> None:
        """Display password security best practices."""
        tips = """
╔════════════════════════════════════════════════════════════╗
║                    PASSWORD SECURITY TIPS                  ║
╚════════════════════════════════════════════════════════════╝

1. LENGTH MATTERS
   • Use at least 12 characters (16+ recommended)
   • Longer passwords are exponentially harder to crack

2. USE VARIETY
   • Mix uppercase, lowercase, numbers, and symbols
   • Each character type increases password space

3. AVOID PATTERNS
   • Don't use dictionary words, names, or dates
   • Avoid keyboard patterns (qwerty, 123456)
   • No repeated characters (aaa, 111)

4. UNIQUE PASSWORDS
   • Never reuse passwords across accounts
   • One breach shouldn't compromise all accounts

5. USE A PASSWORD MANAGER
   • Store passwords securely
   • Generate strong unique passwords easily
   • Access across all devices

6. ENABLE 2FA
   • Add second authentication factor
   • Protects even if password is compromised

7. REGULAR UPDATES
   • Change passwords for sensitive accounts periodically
   • Update immediately if breach suspected

8. PASSPHRASES
   • Consider memorable passphrases (4+ random words)
   • Example: "correct-horse-battery-staple"
   • Easier to remember, harder to crack

9. AVOID PERSONAL INFO
   • Don't use birthdays, names, or addresses
   • Attackers can easily find this information

10. BE WARY OF PHISHING
    • Never enter passwords on suspicious websites
    • Check URL before entering credentials

╔════════════════════════════════════════════════════════════╗
        """
        print(tips)


