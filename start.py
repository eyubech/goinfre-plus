#!/usr/bin/env python3

import os
import sys
import time
import socket
import qrcode
from typing import Callable, Dict, Optional
import platform
from datetime import datetime
import subprocess
from PIL import Image
import threading
import signal

class Colors:
    """ANSI color codes for terminal output styling"""
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class QRCodeGenerator:
    """Generate and display QR codes in the terminal"""
    
    @staticmethod
    def get_terminal_size():
        return os.get_terminal_size()

    @staticmethod
    def generate_terminal_qr(url: str) -> str:
        """Generate QR code and convert to terminal-friendly ASCII art"""
        qr = qrcode.QRCode(version=1, box_size=1, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        
        # Convert QR code to ASCII art
        matrix = qr.get_matrix()
        ascii_art = []
        
        for row in matrix:
            line = ""
            for cell in row:
                if cell:
                    line += "██"
                else:
                    line += "  "
            ascii_art.append(line)
            
        return "\n".join(ascii_art)

class DjangoServer:
    """Manage Django server operations"""
    def __init__(self, port: int = 4242):
        self.port = port
        self.process = None
        self.url = None

    def get_ip(self) -> str:
        """Get the host machine's IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start(self) -> str:
        """Start Django server and return the URL"""
        ip = self.get_ip()
        self.url = f"http://{ip}:{self.port}"
        
        # Start Django server in a separate thread
        self.process = subprocess.Popen(
            [sys.executable, "manage.py", "runserver", f"{ip}:{self.port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return self.url

    def stop(self):
        """Stop the Django server"""
        if self.process:
            self.process.terminate()
            self.process.wait()

class GoinfrePlus:
    def __init__(self):
        self.operations: Dict[str, Callable] = {
            '1': self.imac_only,
            '2': self.mac_to_mac,
            '3': self.exit_program
        }
        self.current_operation: Optional[str] = None
        self.django_server = DjangoServer()
        self.qr_generator = QRCodeGenerator()
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n")
        self.print_status("Operation interrupted by user", "warning")
        self.django_server.stop()
        self.exit_program()

    def print_banner(self) -> None:
        """Display the Goinfre Plus banner with animation"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        banner = """
   ▄██████▄   ▄██████▄   ▄█  ███▄▄▄▄      ▄████████    ▄████████    ▄████████ 
  ███    ███ ███    ███ ███  ███▀▀▀██▄   ███    ███   ███    ███   ███    ███ 
  ███    █▀  ███    ███ ███▌ ███   ███   ███    █▀    ███    ███   ███    █▀  
 ▄███        ███    ███ ███▌ ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▄  ███        
▀▀███ ████▄  ███    ███ ███▌ ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ▀███████████ 
  ███    ███ ███    ███ ███  ███   ███   ███    █▄  ▀███████████          ███ 
  ███    ███ ███    ███ ███  ███   ███   ███    ███   ███    ███    ▄█    ███ 
  ████████▀   ▀██████▀  █▀    ▀█   █▀    ██████████   ███    ███  ▄████████▀  
                                                       ███    ███              
"""
        for line in banner.split('\n'):
            print(line)
            time.sleep(0.05)
        print(f"{Colors.END}")

    def print_loading(self, message: str, duration: float = 0.1) -> None:
        """Display a loading animation with a message"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        for _ in range(10):  # Show animation for 10 cycles
            for char in chars:
                sys.stdout.write(f'\r{Colors.CYAN}{message} {char}{Colors.END}')
                sys.stdout.flush()
                time.sleep(duration)

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
        """Display the main menu with animation"""
        menu_items = [
            f"\n{Colors.YELLOW}{Colors.BOLD}Choose Operation:{Colors.END}",
            f"{Colors.CYAN}1. iMac Only{Colors.END}",
            f"{Colors.CYAN}2. Mac to Mac{Colors.END}",
            f"{Colors.CYAN}3. Exit{Colors.END}"
        ]
        
        for item in menu_items:
            print(item)
            time.sleep(0.1)

    def imac_only(self) -> None:
        """Placeholder for iMac only operation"""
        self.print_status("iMac only operation will be implemented by user", "warning")
        pass

    def mac_to_mac(self) -> None:
        """Handle Mac to Mac transfer operation with Django server"""
        try:
            self.print_loading("Starting Django server")
            url = self.django_server.start()
            
            # Wait for server to start
            time.sleep(2)
            
            # Generate and display QR code
            self.print_status("Server started successfully!", "success")
            print(f"\n{Colors.YELLOW}{Colors.BOLD}Server URL: {url}{Colors.END}")
            
            print(f"\n{Colors.CYAN}{Colors.BOLD}Scan QR Code to access:{Colors.END}")
            qr_code = self.qr_generator.generate_terminal_qr(url)
            print(f"{Colors.BLUE}{qr_code}{Colors.END}")
            
            print(f"\n{Colors.YELLOW}Press Ctrl+C to stop the server{Colors.END}")
            
            # Keep the server running
            while True:
                time.sleep(1)
                
        except Exception as e:
            self.print_status(f"Error: {str(e)}", "error")
        finally:
            self.django_server.stop()

    def exit_program(self) -> None:
        """Exit the program with animation"""
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
            self.signal_handler(None, None)
        except Exception as e:
            self.print_status(f"An error occurred: {str(e)}", "error")
            self.django_server.stop()
            self.exit_program()

def main():
    """Entry point of the program"""
    app = GoinfrePlus()
    app.run()

if __name__ == "__main__":
    main()