import queue
import threading
import logging

class UltronBus:
    def __init__(self):
        # Nessary  Channel
        self.channels = {
            "UI_DISPLAY": queue.Queue(),          # UI ကို စာသားပြန်ပို့ရန်
            "MESH_OUT": queue.Queue(),            # LoRa/Network သို့ ပို့ရန်
            "MESH_IN": queue.Queue(),             # Network မှ ဝင်လာသည်များကို လက်ခံရန်
            "LEARNER_IN": queue.Queue(),          # RAG/Memory ထဲ သိမ်းရန်
            "SYSTEM_LOG": queue.Queue(),          # Debug log များအတွက်
            "SYSTEM_SHUTDOWN":queue.Queue(),      #shutdown
            "USER_INPUT_RECEIVED": queue.Queue()  # User ရိုက်လိုက်သော Command များ
        }
        self.listeners = {}
        self.active = True
        self._lock = threading.Lock() # Thread-safe ဖြစ်စေရန်

    def subscribe(self, channel_name, callback):
        """Channel တစ်ခုခုမှာ data တက်လာရင် callback function ကို ချက်ချင်းခေါ်ပေးရန်"""
        with self._lock:
            if channel_name not in self.listeners:
                self.listeners[channel_name] = []
            self.listeners[channel_name].append(callback)

    def publish(self, channel_name, data):
        """Data ပို့ခြင်း - Listener ရှိရင် ချက်ချင်းပို့မည်၊ မရှိရင် Queue ထဲ ထည့်ထားမည်"""
        if channel_name not in self.channels:
            print(f"[!] Critical Error: Channel {channel_name} does not exist!")
            return

        # ၁။ Queue ထဲ ထည့်ထားခြင်း (Backup)
        self.channels[channel_name].put(data)

        # ၂။ Listener (Callback) များရှိရင် ချက်ချင်း အကြောင်းကြားခြင်း
        with self._lock:
            if channel_name in self.listeners:
                for callback in self.listeners[channel_name]:
                    try:
                        # Thread အသစ်ဖြင့် callback ကို run ရန် (Bus ပိတ်မသွားစေရန်)
                        threading.Thread(target=callback, args=(data,), daemon=True).start()
                    except Exception as e:
                        print(f"[!] Bus Callback Error on {channel_name}: {e}")

    def listen(self, channel_name, timeout=None):
        """Queue ထဲမှ data ကို ဆွဲထုတ်ဖတ်ခြင်း (Blocking with Timeout)"""
        if channel_name in self.channels:
            try:
                return self.channels[channel_name].get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def clear_queue(self, channel_name):
        """Queue ဟောင်းများကို ရှင်းထုတ်ခြင်း"""
        if channel_name in self.channels:
            with self.channels[channel_name].mutex:
                self.channels[channel_name].queue.clear()

# Global Instance
bus = UltronBus()
