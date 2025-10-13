"""
Password Security Tool - Main Entry Point

Author: Emtiaz Sid
License: MIT
Version: 1.0.0
"""

import sys
from src.tool import PasswordSecurityTool


def main():
    """Main entry point for the application."""
    try:
        tool = PasswordSecurityTool()
        tool.display_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()