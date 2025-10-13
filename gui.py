"""
Password Security Tool - GUI Version
A beautiful graphical interface for password security.

Author: Your Name
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip  # For clipboard functionality
from src.tool import PasswordSecurityTool
from src.models import StrengthLevel


class PasswordSecurityGUI:
    """Graphical User Interface for Password Security Tool."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Password Security Tool")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Initialize the tool
        self.tool = PasswordSecurityTool()
        
        # Color scheme
        self.colors = {
            'bg': '#f0f4f8',
            'primary': '#2563eb',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'white': '#ffffff',
            'text': '#1e293b'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg'])
        
        # Create main container
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Header
        self.create_header()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_checker_tab()
        self.create_generator_tab()
        self.create_tips_tab()
        
    def create_header(self):
        """Create header section."""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Password Security Tool",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=20)
        
    def create_checker_tab(self):
        """Create password checker tab."""
        checker_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(checker_frame, text="  Password Checker  ")
        
        # Title
        title = tk.Label(
            checker_frame,
            text="Check Password Strength",
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(checker_frame, bg=self.colors['bg'])
        input_frame.pack(pady=10, padx=40, fill='x')
        
        tk.Label(
            input_frame,
            text="Enter Password:",
            font=('Arial', 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=5)
        
        # Password entry with show/hide
        entry_container = tk.Frame(input_frame, bg=self.colors['white'])
        entry_container.pack(fill='x')
        
        self.password_entry = tk.Entry(
            entry_container,
            font=('Arial', 14),
            show='•',
            relief='flat',
            bd=5
        )
        self.password_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        self.password_entry.bind('<KeyRelease>', self.on_password_change)
        
        # Show/Hide button
        self.show_password_var = tk.BooleanVar(value=False)
        self.show_btn = tk.Button(
            entry_container,
            text="👁",
            font=('Arial', 12),
            command=self.toggle_password_visibility,
            relief='flat',
            bg=self.colors['white'],
            cursor='hand2'
        )
        self.show_btn.pack(side='right', padx=5)
        
        # Check button
        check_btn = tk.Button(
            input_frame,
            text="Analyze Password",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            command=self.check_password,
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10
        )
        check_btn.pack(pady=10)
        
        # Results frame
        self.results_frame = tk.Frame(checker_frame, bg=self.colors['white'], relief='ridge', bd=2)
        self.results_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Placeholder
        self.results_placeholder = tk.Label(
            self.results_frame,
            text="Enter a password above to see the analysis",
            font=('Arial', 12),
            bg=self.colors['white'],
            fg=self.colors['secondary']
        )
        self.results_placeholder.pack(pady=50)
        
    def create_generator_tab(self):
        """Create password generator tab."""
        generator_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(generator_frame, text="  Password Generator  ")
        
        # Title
        title = tk.Label(
            generator_frame,
            text="Generate Secure Password",
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title.pack(pady=20)
        
        # Settings frame
        settings_frame = tk.LabelFrame(
            generator_frame,
            text="Password Settings",
            font=('Arial', 12, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=20,
            pady=20
        )
        settings_frame.pack(pady=10, padx=40, fill='x')
        
        # Length slider
        length_frame = tk.Frame(settings_frame, bg=self.colors['white'])
        length_frame.pack(fill='x', pady=10)
        
        tk.Label(
            length_frame,
            text="Password Length:",
            font=('Arial', 11),
            bg=self.colors['white']
        ).pack(side='left')
        
        self.length_var = tk.IntVar(value=16)
        self.length_label = tk.Label(
            length_frame,
            text="16",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        self.length_label.pack(side='right')
        
        self.length_slider = tk.Scale(
            settings_frame,
            from_=8,
            to=32,
            orient='horizontal',
            variable=self.length_var,
            command=self.update_length_label,
            bg=self.colors['white'],
            highlightthickness=0,
            troughcolor=self.colors['bg']
        )
        self.length_slider.pack(fill='x', pady=5)
        
        # Checkboxes
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        checkbox_frame = tk.Frame(settings_frame, bg=self.colors['white'])
        checkbox_frame.pack(pady=10)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Lowercase (a-z)",
            variable=self.use_lowercase,
            font=('Arial', 10),
            bg=self.colors['white']
        ).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Uppercase (A-Z)",
            variable=self.use_uppercase,
            font=('Arial', 10),
            bg=self.colors['white']
        ).grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Numbers (0-9)",
            variable=self.use_digits,
            font=('Arial', 10),
            bg=self.colors['white']
        ).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Symbols (!@#$)",
            variable=self.use_symbols,
            font=('Arial', 10),
            bg=self.colors['white']
        ).grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        # Generate button
        generate_btn = tk.Button(
            generator_frame,
            text="🔑 Generate Password",
            font=('Arial', 12, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['white'],
            command=self.generate_password,
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10
        )
        generate_btn.pack(pady=15)
        
        # Generated password display
        display_frame = tk.LabelFrame(
            generator_frame,
            text="Generated Password",
            font=('Arial', 12, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=20,
            pady=20
        )
        display_frame.pack(pady=10, padx=40, fill='x')
        
        self.generated_password_var = tk.StringVar(value="Click 'Generate Password' to create one")
        password_display = tk.Entry(
            display_frame,
            textvariable=self.generated_password_var,
            font=('Courier', 14, 'bold'),
            justify='center',
            state='readonly',
            relief='flat',
            bg=self.colors['bg']
        )
        password_display.pack(fill='x', pady=10)
        
        # Copy button
        copy_btn = tk.Button(
            display_frame,
            text="📋 Copy to Clipboard",
            font=('Arial', 11),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            command=self.copy_password,
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        copy_btn.pack()
        
        # Passphrase section
        passphrase_frame = tk.LabelFrame(
            generator_frame,
            text="Or Generate Passphrase",
            font=('Arial', 12, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=20,
            pady=20
        )
        passphrase_frame.pack(pady=10, padx=40, fill='x')
        
        passphrase_btn = tk.Button(
            passphrase_frame,
            text="Generate Passphrase",
            font=('Arial', 11),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            command=self.generate_passphrase,
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        passphrase_btn.pack()
        
    def create_tips_tab(self):
        """Create security tips tab."""
        tips_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tips_frame, text="  Security Tips  ")
        
        # Title
        title = tk.Label(
            tips_frame,
            text="Password Security Best Practices",
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title.pack(pady=20)
        
        # Tips text
        tips_text = scrolledtext.ScrolledText(
            tips_frame,
            font=('Arial', 11),
            wrap='word',
            bg=self.colors['white'],
            relief='flat',
            padx=20,
            pady=20
        )
        tips_text.pack(pady=10, padx=40, fill='both', expand=True)
        
        tips_content = """
🔐 PASSWORD SECURITY TIPS

1. LENGTH MATTERS
   • Use at least 12 characters (16+ recommended)
   • Longer passwords are exponentially harder to crack
   • Each additional character dramatically increases security

2. USE VARIETY
   • Mix uppercase letters (A-Z)
   • Mix lowercase letters (a-z)
   • Include numbers (0-9)
   • Add special characters (!@#$%^&*)

3. AVOID PATTERNS
   • Don't use dictionary words
   • Avoid personal information (birthdays, names)
   • No keyboard patterns (qwerty, 123456)
   • Avoid repeated characters (aaa, 111)

4. UNIQUE PASSWORDS
   • Never reuse passwords across accounts
   • One breach shouldn't compromise all accounts
   • Use different passwords for work and personal

5. USE A PASSWORD MANAGER
   • Store passwords securely and encrypted
   • Generate strong unique passwords easily
   • Access passwords across all devices
   • Popular options: Bitwarden, 1Password, LastPass

6. ENABLE TWO-FACTOR AUTHENTICATION (2FA)
   • Adds a second layer of security
   • Protects even if password is compromised
   • Use authenticator apps over SMS when possible

7. REGULAR UPDATES
   • Change passwords for sensitive accounts periodically
   • Update immediately if you suspect a breach
   • Change default passwords on all devices

8. PASSPHRASES
   • Consider memorable passphrases (4+ random words)
   • Example: "correct-horse-battery-staple"
   • Easier to remember, harder to crack
   • Can be more secure than complex passwords

9. AVOID PERSONAL INFO
   • Don't use birthdays, anniversaries, or names
   • Attackers can easily find this information online
   • Avoid pet names, favorite teams, or hobbies

10. BE WARY OF PHISHING
    • Never enter passwords on suspicious websites
    • Check URL carefully before entering credentials
    • Watch for spelling mistakes in domains
    • Don't click links in unexpected emails

COMMON PASSWORD MYTHS:

❌ MYTH: Changing passwords frequently makes you safer
✅ FACT: Focus on strong, unique passwords over frequent changes

❌ MYTH: Complex but short passwords are secure
✅ FACT: Length is more important than complexity

❌ MYTH: Password managers are risky
✅ FACT: They're much safer than reusing passwords

REMEMBER:
The best password is one that's:
• Long (16+ characters)
• Random (no patterns)
• Unique (used nowhere else)
• Stored securely (in a password manager)

Stay safe online! 🛡️
        """
        
        tips_text.insert('1.0', tips_content)
        tips_text.config(state='disabled')
        
    def toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.show_password_var.get():
            self.password_entry.config(show='')
            self.show_btn.config(text='👁‍🗨')
            self.show_password_var.set(False)
        else:
            self.password_entry.config(show='•')
            self.show_btn.config(text='👁')
            self.show_password_var.set(True)
            
    def on_password_change(self, event=None):
        """Handle password entry change for real-time feedback."""
        password = self.password_entry.get()
        if password:
            self.check_password()
            
    def check_password(self):
        """Check password strength and display results."""
        password = self.password_entry.get()
        
        if not password:
            messagebox.showwarning("Empty Password", "Please enter a password to check.")
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Analyze password
        analysis = self.tool.checker.check_strength(password)
        
        # Strength label with color
        strength_colors = {
            StrengthLevel.VERY_WEAK: self.colors['danger'],
            StrengthLevel.WEAK: '#f97316',
            StrengthLevel.FAIR: self.colors['warning'],
            StrengthLevel.GOOD: '#84cc16',
            StrengthLevel.STRONG: self.colors['success'],
            StrengthLevel.VERY_STRONG: '#059669'
        }
        
        strength_color = strength_colors.get(analysis.strength, self.colors['secondary'])
        
        tk.Label(
            self.results_frame,
            text=f"Strength: {analysis.strength.name}",
            font=('Arial', 16, 'bold'),
            bg=self.colors['white'],
            fg=strength_color
        ).pack(pady=10)
        
        # Progress bar
        progress_frame = tk.Frame(self.results_frame, bg=self.colors['white'])
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        canvas = tk.Canvas(progress_frame, height=30, bg=self.colors['bg'], highlightthickness=0)
        canvas.pack(fill='x')
        
        bar_width = (analysis.score / 10) * canvas.winfo_reqwidth()
        if bar_width < 50:
            bar_width = 50
        canvas.create_rectangle(0, 0, bar_width, 30, fill=strength_color, outline='')
        
        # Stats
        stats_frame = tk.Frame(self.results_frame, bg=self.colors['white'])
        stats_frame.pack(pady=10)
        
        tk.Label(
            stats_frame,
            text=f"Score: {analysis.score}/10",
            font=('Arial', 12),
            bg=self.colors['white']
        ).grid(row=0, column=0, padx=20, pady=5)
        
        tk.Label(
            stats_frame,
            text=f"Entropy: {analysis.entropy} bits",
            font=('Arial', 12),
            bg=self.colors['white']
        ).grid(row=0, column=1, padx=20, pady=5)
        
        tk.Label(
            stats_frame,
            text=f"Time to Crack: {analysis.time_to_crack}",
            font=('Arial', 12),
            bg=self.colors['white']
        ).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Feedback
        if analysis.feedback:
            feedback_frame = tk.LabelFrame(
                self.results_frame,
                text="Suggestions for Improvement",
                font=('Arial', 11, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['text']
            )
            feedback_frame.pack(pady=10, padx=20, fill='x')
            
            for item in analysis.feedback:
                tk.Label(
                    feedback_frame,
                    text=f"• {item}",
                    font=('Arial', 10),
                    bg=self.colors['white'],
                    fg=self.colors['text'],
                    anchor='w',
                    justify='left'
                ).pack(anchor='w', padx=10, pady=2)
                
    def update_length_label(self, value):
        """Update length label when slider moves."""
        self.length_label.config(text=str(int(float(value))))
        
    def generate_password(self):
        """Generate a random password."""
        try:
            password = self.tool.generator.generate(
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase.get(),
                use_uppercase=self.use_uppercase.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get()
            )
            self.generated_password_var.set(password)
            messagebox.showinfo("Success", "Password generated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def generate_passphrase(self):
        """Generate a passphrase."""
        passphrase = self.tool.generator.generate_passphrase(word_count=4)
        self.generated_password_var.set(passphrase)
        messagebox.showinfo("Success", "Passphrase generated successfully!")
        
    def copy_password(self):
        """Copy generated password to clipboard."""
        password = self.generated_password_var.get()
        if password and password != "Click 'Generate Password' to create one":
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Copied", "Password copied to clipboard!")
            except:
                # Fallback if pyperclip doesn't work
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Generate a password first!")


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    app = PasswordSecurityGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()