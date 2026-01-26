import sys
import time
import threading
import signal
from pathlib import Path

# V7 Module Imports
# (sys.path ကို ညှိပေးထားပါတယ်၊ ဒါမှ v7 folder ထဲက module တွေကို လှမ်းခေါ်လို့ရမှာ)
sys.path.append(str(Path(__file__).parent / "v7"))

from core.bus import bus
from core.engine import UltronEngine
from core.utils import print_banner, log_system

# Global State for clean shutdown
running = True

def signal_handler(sig, frame):
    """Ctrl+C နှိပ်ရင် စနစ်တကျ ပိတ်ဖို့"""
    global running
    print("\n\n[!] Force Shutdown Sequence Initiated...")
    bus.publish("SYSTEM_SHUTDOWN", {"reason": "user_interrupt"})
    running = False
    sys.exit(0)

def background_listener():
    """Bus ပေါ်က Message တွေကို နားထောင်ပြီး UI မှာ ပြပေးမယ့် Thread"""
    def on_ui_message(data):
        # UI Update လိုမျိုး သဘောထားပါ
        if isinstance(data, dict) and "msg" in data:
            print(f"\r[SYSTEM] >> {data['msg']}\n[Query] > ", end="")

    bus.subscribe("UI_DISPLAY", on_ui_message)

    while running:
        time.sleep(1)

def main():
    # ၁။ Banner နဲ့ System Check
    print_banner()
    log_system("INFO","Initializing V7 Neural Architecture...")

    # ၂။ Engine (The Brain) ကို စတင်ခြင်း
    try:
        engine = UltronEngine()
        engine.boot_up() # Memory load, Peer Sync, RAG check
        log_system("SUCCESS","Engine Online. Swarm is ready.")
    except Exception as e:
        log_system(f"ERROR","CRITICAL ERROR during Engine Boot: {e}", level="ERROR")
        sys.exit(1)

    # ၃။ Background Listener (UI Updates)
    listener = threading.Thread(target=background_listener, daemon=True)
    listener.start()

    # ၄။ Main Input Loop (Non-blocking style logic)
    signal.signal(signal.SIGINT, signal_handler)

    print("\n[!] ULTRON V7 IS LIVE. Waiting for commands...")
    print("Type 'exit' to quit, 'swarm' to activate swarm mode.\n")

    while running:
        try:
            user_input = input("[Query] > ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("[*] Saving Memory & Shutting down...")
                engine.shutdown()
                break

            # ၅။ Task ကို Engine ဆီ ပို့ခြင်း
            # ဒါက မင်းရဲ့ RAG, Generate, Execute အားလုံးကို Engine က စီမံမှာ
            bus.publish("USER_INPUT_RECEIVED", {"command": user_input})

            # Engine ရဲ့ တုံ့ပြန်မှုကို စောင့်မနေဘဲ (Async) ဖြစ်နိုင်သလို
            # ရိုးရှင်းအောင် Direct Call လည်း သုံးနိုင်ပါတယ်:
            result = engine.process_request(user_input)

            if result.get("status") == "success":
                print(f"\n[+] Result:\n{result.get('output', 'Task Completed')}")
                if result.get("file_generated"):
                    print(f"[>] File saved at: {result['file_generated']}")
            else:
                print(f"\n[!] Operation Failed: {result.get('error')}")

        except KeyboardInterrupt:
            signal_handler(None, None)
        except Exception as e:
            print(f"[!] Runtime Error: {e}")

if __name__ == "__main__":
    main()
