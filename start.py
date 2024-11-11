#!/usr/bin/env python3

import os
import sys
import time
from typing import Callable, Dict, Optional
import platform
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output styling"""
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class GoinfrePlus:
    def __init__(self):
        self.operations: Dict[str, Callable] = {
            '1': self.imac_only,
            '2': self.mac_to_mac,
            '3': self.exit_program
        }
        self.current_operation: Optional[str] = None

    def print_banner(self) -> None:
        """Display the Goinfre Plus banner"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("""
   ▄██████▄   ▄██████▄   ▄█  ███▄▄▄▄      ▄████████    ▄████████    ▄████████ 
  ███    ███ ███    ███ ███  ███▀▀▀██▄   ███    ███   ███    ███   ███    ███ 
  ███    █▀  ███    ███ ███▌ ███   ███   ███    █▀    ███    ███   ███    █▀  
 ▄███        ███    ███ ███▌ ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▄  ███        
▀▀███ ████▄  ███    ███ ███▌ ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ▀███████████ 
  ███    ███ ███    ███ ███  ███   ███   ███    █▄  ▀███████████          ███ 
  ███    ███ ███    ███ ███  ███   ███   ███    ███   ███    ███    ▄█    ███ 
  ████████▀   ▀██████▀  █▀    ▀█   █▀    ██████████   ███    ███  ▄████████▀  
                                                       ███    ███              
        """)
        print(f"{Colors.END}")

    def print_loading(self, message: str, duration: float = 0.1) -> None:
        """Display a loading animation with a message"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        for char in chars:
            sys.stdout.write(f'\r{Colors.CYAN}{message} {char}{Colors.END}')
            sys.stdout.flush()
            time.sleep(duration)
        print()

    def print_status(self, message: str, status: str = "info") -> None:
        """Print a formatted status message"""
        color = {
            "success": Colors.GREEN,
            "error": Colors.RED,
            "info": Colors.BLUE,
            "warning": Colors.YELLOW
        }.get(status, Colors.BLUE)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] {message}{Colors.END}")

    def show_menu(self) -> None:
        """Display the main menu"""
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Choose Operation:{Colors.END}")
        print(f"{Colors.CYAN}1. iMac Only{Colors.END}")
        print(f"{Colors.CYAN}2. Mac to Mac{Colors.END}")
        print(f"{Colors.CYAN}3. Exit{Colors.END}")

    def imac_only(self) -> None:
        """Placeholder for iMac only operation"""
        self.print_status("iMac only operation will be implemented by user", "warning")
        # TODO: Implement your custom iMac only operation logic here
        pass

    def mac_to_mac(self) -> None:
        """Placeholder for Mac to Mac transfer operation"""
        self.print_status("Mac to Mac transfer will be implemented by user", "warning")
        # TODO: Implement your custom Mac to Mac transfer logic here
        pass

    def exit_program(self) -> None:
        """Exit the program with a goodbye message"""
        self.print_loading("Cleaning up")
        print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using Goinfre Plus!{Colors.END}")
        sys.exit(0)

    def run(self) -> None:
        """Main program loop"""
        try:
            self.print_banner()
            self.print_status("Welcome to Goinfre Plus!", "success")
            
            while True:
                self.show_menu()
                choice = input(f"\n{Colors.YELLOW}Select option (1-3): {Colors.END}")
                
                if choice in self.operations:
                    self.current_operation = choice
                    self.print_loading("Initializing operation")
                    self.operations[choice]()
                else:
                    self.print_status("Invalid option. Please try again.", "error")

        except KeyboardInterrupt:
            print("\n")
            self.print_status("Operation interrupted by user", "warning")
            self.exit_program()
        except Exception as e:
            self.print_status(f"An error occurred: {str(e)}", "error")
            self.exit_program()

def main():
    """Entry point of the program"""
    app = GoinfrePlus()
    app.run()

if __name__ == "__main__":
    main()