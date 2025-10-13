# 🔐 Password Security Tool

> **A professional-grade password strength checker and secure password generator written in Python**

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

---

## ✨ Features

### 🛡️ **Password Strength Analysis**
- **Multi-factor security evaluation** with detailed scoring
- **Entropy calculation** in bits for cryptographic strength
- **Pattern detection** (common passwords, keyboard patterns, repetitions)
- **Time-to-crack estimation** based on modern attack vectors
- **Detailed improvement feedback** for weak passwords

### 🔑 **Secure Password Generation**
- **Cryptographically secure** random generation using Python's `secrets` module
- **Fully customizable** length and character types
- **Memorable passphrase** generation
- **PIN code** generation
- **Batch generation** for multiple passwords at once

### 💻 **Dual Interface**
- **Interactive CLI** with beautiful menu system
- **Modern GUI** with tabbed interface (optional)
- **Clear analysis reports** with color-coded results
- **Built-in security tips** and best practices

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/noobest/password-security-tool.git
cd password-security-tool

# Run the CLI tool
python main.py

# Or run the GUI version
pip install pyperclip
python gui.py
```

### Requirements

- **Python 3.6+** (no external dependencies for CLI version!)
- **pyperclip** (optional, for GUI clipboard functionality)

---

## 📖 Usage

### 🖥️ Interactive CLI Mode

```bash
python main.py
```

You'll see a menu with these options:

1. ✅ **Check Password Strength** - Analyze any password
2. 🔑 **Generate Secure Password** - Create random passwords
3. 📝 **Generate Passphrase** - Create memorable passphrases
4. 🎲 **Generate Multiple Passwords** - Batch generation
5. 💡 **Security Tips** - Learn best practices
6. 🚪 **Exit** - Close the application

---

### 🎨 GUI Mode

```bash
python gui.py
```

**Features:**
- 🎯 **Password Checker Tab** - Real-time strength analysis with visual meter
- 🎲 **Password Generator Tab** - Customizable generation with sliders
- 💡 **Security Tips Tab** - Comprehensive security guidelines

![GUI Screenshot](https://via.placeholder.com/800x500?text=Password+Security+Tool+GUI)

---

### 🐍 As a Python Module

```python
from src import PasswordSecurityTool

# Initialize the tool
tool = PasswordSecurityTool()

# ✅ Check password strength
analysis = tool.analyze_password("MyP@ssw0rd123", display=False)
print(f"💪 Strength: {analysis.strength.name}")
print(f"📊 Score: {analysis.score}/10")
print(f"🔒 Entropy: {analysis.entropy} bits")
print(f"⏱️ Time to crack: {analysis.time_to_crack}")

# 🔑 Generate a secure password
password = tool.generator.generate(
    length=20,
    use_symbols=True
)
print(f"🎲 Generated: {password}")

# 📝 Generate a memorable passphrase
passphrase = tool.generator.generate_passphrase(
    word_count=5,
    separator="-",
    capitalize=True
)
print(f"✨ Passphrase: {passphrase}")
```

---

## 📁 Project Structure

```
password-security-tool/
├── 📂 src/
│   ├── 📄 __init__.py       # Package initialization
│   ├── 📄 models.py         # Data models (StrengthLevel, PasswordAnalysis)
│   ├── 📄 checker.py        # Password strength checker logic
│   ├── 📄 generator.py      # Secure password generator
│   └── 📄 tool.py           # Main tool interface
├── 📄 main.py               # 🖥️ CLI application entry point
├── 📄 gui.py                # 🎨 GUI application (optional)
├── 📄 README.md             # 📖 This file
├── 📄 requirements.txt      # 📦 Dependencies
├── 📄 .gitignore           # 🚫 Git ignore rules
└── 📄 LICENSE              # ⚖️ MIT License
```

---

## 🎯 Examples

### Example 1: Batch Password Analysis

```python
from src import PasswordSecurityTool

tool = PasswordSecurityTool()

passwords = ["password123", "MyP@ssw0rd2024", "correct-horse-battery-staple"]

for pwd in passwords:
    analysis = tool.analyze_password(pwd, display=False)
    print(f"🔐 {pwd}")
    print(f"   💪 {analysis.strength.name} | ⏱️ {analysis.time_to_crack}")
```

**Output:**
```
🔐 password123
   💪 VERY_WEAK | ⏱️ Instant

🔐 MyP@ssw0rd2024
   💪 GOOD | ⏱️ 2 years

🔐 correct-horse-battery-staple
   💪 STRONG | ⏱️ 54 years
```

---

### Example 2: Generate Multiple Passwords

```python
from src import PasswordGenerator

generator = PasswordGenerator()

# Generate 5 passwords for different purposes
passwords = {
    '📧 Email': generator.generate(16, use_symbols=True),
    '🏦 Bank': generator.generate(20, use_symbols=True),
    '📱 Social': generator.generate(14, use_symbols=False),
    '💼 Work': generator.generate(16, use_symbols=False),
    '🎮 Gaming': generator.generate(12, use_symbols=False)
}

for account, pwd in passwords.items():
    print(f"{account}: {pwd}")
```

---

### Example 3: Integration with User Registration

```python
from src import PasswordSecurityTool, StrengthLevel

def register_user(username: str, password: str) -> bool:
    """Validate password strength during user registration."""
    tool = PasswordSecurityTool()
    analysis = tool.analyze_password(password, display=False)
    
    # Require at least GOOD strength
    if analysis.strength.value < StrengthLevel.GOOD.value:
        print(f"❌ Password too weak: {analysis.strength.name}")
        print("💡 Suggestions:")
        for feedback in analysis.feedback:
            print(f"   • {feedback}")
        return False
    
    print(f"✅ User '{username}' registered successfully!")
    print(f"💪 Password strength: {analysis.strength.name}")
    return True

# Test
register_user("john_doe", "weak123")           # ❌ Fails
register_user("john_doe", "MyStr0ng!Pass2024") # ✅ Success
```

---

## 🔧 API Reference

### PasswordStrengthChecker

```python
from src import PasswordStrengthChecker

checker = PasswordStrengthChecker()
analysis = checker.check_strength("your_password_here")
```

**Returns:** `PasswordAnalysis` object with:
- **`strength`** - StrengthLevel enum (VERY_WEAK to VERY_STRONG)
- **`score`** - Integer score (0-10+)
- **`entropy`** - Float entropy in bits
- **`feedback`** - List[str] of improvement suggestions
- **`time_to_crack`** - String estimate of crack time

---

### PasswordGenerator

```python
from src import PasswordGenerator

generator = PasswordGenerator()
```

**Methods:**

| Method | Description | Returns |
|--------|-------------|---------|
| `generate(length, ...)` | Generate secure random password | `str` |
| `generate_passphrase(word_count, ...)` | Generate memorable passphrase | `str` |
| `generate_pin(length)` | Generate numeric PIN | `str` |
| `generate_multiple(count, ...)` | Generate multiple passwords | `List[str]` |

---

## 🧪 Testing

### Manual Testing

```bash
python main.py
```

**Test these passwords:**
- ❌ `"password"` → VERY_WEAK
- ⚠️ `"Password123"` → FAIR
- ✅ `"MyP@ssw0rd2024!"` → STRONG

### Unit Tests

```python
# tests/test_checker.py
import unittest
from src import PasswordStrengthChecker, StrengthLevel

class TestPasswordChecker(unittest.TestCase):
    def setUp(self):
        self.checker = PasswordStrengthChecker()
    
    def test_weak_password(self):
        result = self.checker.check_strength("password")
        self.assertEqual(result.strength, StrengthLevel.VERY_WEAK)
    
    def test_strong_password(self):
        result = self.checker.check_strength("MyStr0ng!P@ss2024")
        self.assertIn(result.strength, [
            StrengthLevel.STRONG,
            StrengthLevel.VERY_STRONG
        ])

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest discover tests
```

---

## 🚀 Deployment

### Create Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --name password-tool main.py

# Executable will be in dist/password-tool
```

### Docker Container (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
```

```bash
docker build -t password-security-tool .
docker run -it password-security-tool
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| ❌ `ModuleNotFoundError: No module named 'src'` | ✅ Run from project root directory, ensure `src/__init__.py` exists |
| ❌ Password generation fails | ✅ Select at least one character type |
| ❌ GUI doesn't open | ✅ Install pyperclip: `pip install pyperclip` |
| ❌ Virtual environment issues | ✅ Activate venv: `venv\Scripts\Activate.ps1` (Windows) |

---

## 🔮 Roadmap

### Planned Features

- [ ] 🌐 **Breach Database Integration** - Check against Have I Been Pwned API
- [ ] 📊 **Password History Tracking** - Remember generated passwords
- [ ] ⚙️ **Configuration File** - Save user preferences
- [ ] 🌍 **Multi-language Support** - i18n support
- [ ] 💾 **Export Features** - Save to encrypted files
- [ ] 📱 **Mobile App** - React Native version
- [ ] 🔌 **Browser Extension** - Chrome/Firefox integration
- [ ] 🎨 **Themes** - Dark/light mode for GUI

---

## ⚡ Performance

| Metric | Value |
|--------|-------|
| Password Checking | O(n) where n = password length |
| Password Generation | O(1) - constant time |
| Memory Usage | < 1MB |
| Network Calls | None |

---

## 🔒 Security Standards

This tool implements:

- ✅ **NIST SP 800-63B** - Digital Identity Guidelines
- ✅ **OWASP** - Password Security Best Practices
- ✅ **Shannon Entropy** - Information theory for strength calculation
- ✅ **Cryptographically Secure** - Python's `secrets` module
- ✅ **No Data Collection** - 100% offline, privacy-focused

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 📝 **Commit** your changes
   ```bash
   git commit -m '✨ Add some AmazingFeature'
   ```
4. 📤 **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. 🎉 **Open** a Pull Request

### Guidelines

- Follow **PEP 8** style guidelines
- Add **docstrings** to all functions
- Include **type hints**
- Write **unit tests** for new features
- Update **documentation**

---

## 📜 Changelog

### Version 1.0.0 (2024)

- ✨ Initial release
- 🛡️ Password strength checker with entropy calculation
- 🔑 Secure password generator
- 📝 Passphrase generation
- 💻 Interactive CLI interface
- 🎨 Optional GUI interface
- 📖 Comprehensive documentation

---

## 📞 Support

**Need help? Have questions?**

- 🐛 **Issues:** [Report bugs](https://github.com/noobest/password-security-tool/issues)
- 💬 **Discussions:** [Ask questions](https://github.com/noobest/password-security-tool/discussions)
- 📧 **Email:** siddiqueemtiaz@gmail.com

---

## ⚠️ Disclaimer

This tool is designed for **educational and personal use**. While it implements industry-standard security best practices, for **production environments** always use established, audited password managers like Bitwarden, 1Password, or KeePass.

---

## 📄 License

**MIT License** - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Siddique Emtiaz

---

<div align="center">

### 🎉 Happy Secure Password Generation! 🔐

**Made with ❤️ by [Siddique Emtiaz](https://github.com/noobest)**

⭐ **If this project helped you, please star it!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/noobest/password-security-tool?style=social)](https://github.com/noobest/password-security-tool/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/noobest/password-security-tool?style=social)](https://github.com/noobest/password-security-tool/network/members)

[🐛 Report Bug](https://github.com/noobest/password-security-tool/issues) • [✨ Request Feature](https://github.com/noobest/password-security-tool/issues) • [📖 Documentation](https://github.com/noobest/password-security-tool)

</div>

---

## 🌟 Show Your Support

If this project helped you, please consider:
- ⭐ **Starring** the repository
- 🍴 **Forking** for your own use
- 📢 **Sharing** with others on social media
- 💖 **Contributing** improvements
- ☕ **Buying me a coffee** (optional)

---

**© 2024 Siddique Emtiaz. All rights reserved.**
