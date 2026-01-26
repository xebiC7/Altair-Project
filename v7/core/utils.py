import os
import sys
import time
from datetime import datetime

# ANSI Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m" 

def typing_effect(text, delay=0.03):
    """စာသားတွေကို တစ်လုံးချင်း ရိုက်ပြမည့် Effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_banner():
    """Altair V7 Animated Banner"""
    os.system('clear')
    banner_text = f"""
{CYAN}{BOLD}
 █████  ██      ████████  █████  ██ ██████
██   ██ ██         ██    ██   ██ ██ ██   ██
███████ ██         ██    ███████ ██ ██████
██   ██ ██         ██    ██   ██ ██ ██   ██
██   ██ ███████    ██    ██   ██ ██ ██   ██
                                 V8 - NEXT GEN
{RESET}"""
    print(banner_text)
    typing_effect(f"{GREEN} [SYSTEM]: ALTAIR DECENTRALIZED MESH ACTIVE")
    typing_effect(f"{GREEN} [STATUS]: AIR-GAPPED / NO-INTERNET MODE")
    typing_effect(f"{GREEN} [LOGIC ]: POWERED BY xebiC7")
    print(f"{CYAN}="*50 + f"{RESET}\n")

def log_system(category, message):
    """System Event Log with Colors"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    color = WHITE
    if category == "SUCCESS": color = GREEN
    elif category == "ERROR": color = RED
    elif category == "INFO": color = BLUE
    elif category == "MESH": color = CYAN

    # Log ကို လှအောင် format လုပ်ခြင်း
    print(f"{WHITE}[{timestamp}]{RESET} {color}{BOLD}[{category:<7}]{RESET} {message}")

def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    """အနာဂတ်အတွက် Loading Bar (ဥပမာ- AI model load လုပ်လျှင် သုံးရန်)"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()
