import time
import psutil
import os
import sys
from datetime import datetime
from plyer import notification
from config import BLOCKLIST
from state_manager import StateManager

TARGET_DATE = datetime(2026, 3, 31)

def get_days_remaining():
    now = datetime.now()
    delta = TARGET_DATE - now
    return max(0, delta.days)

def send_doomsday_notification():
    days = get_days_remaining()
    title = f"【警告】人生の分岐点まで残り {days} 日"
    message = f"30歳工場勤務確定まで、あと {days} 日。\nそれでも遊びますか？\n今すぐコードを書け。"
    
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Code-to-Play Warden",
            timeout=10
        )
    except Exception as e:
        print(f"Notification error: {e}")

def active_monitoring():
    """
    Main loop for background monitoring.
    """
    print("Code-to-Play Warden is active.")
    try:
        while True:
            # 1. Check Reward State
            if StateManager.is_reward_active():
                # Reward is active, do nothing (sleep longer to save CPU)
                # print("Reward active. Gaming allowed.") 
                time.sleep(60) 
                continue

            # 2. Reward is NOT active. Scan and Kill.
            # Convert blocklist to lowercase for case-insensitive matching
            blocklist_lower = [name.lower() for name in BLOCKLIST]
            
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() in blocklist_lower:
                        print(f"Detected prohibited process: {proc.info['name']}. TERMINATING.")
                        proc.kill() # Using Force Kill as requested
                        send_doomsday_notification()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # Sleep shorter when in blocking mode to catch startup quickly
            time.sleep(5)

    except KeyboardInterrupt:
        print("Warden stopping... (this should not happen in background mode)")

if __name__ == "__main__":
    # Ensure it's not easily closed if run visibly
    active_monitoring()
