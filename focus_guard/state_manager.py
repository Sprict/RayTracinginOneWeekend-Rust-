import json
import os
import time
import hashlib
import hmac
from config import STATE_FILE, SALT

class StateManager:
    """
    Manages the reward state (expiry time) with integrity checks.
    """

    @staticmethod
    def _calculate_hash(data_str):
        return hmac.new(SALT.encode(), data_str.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def load_state():
        """
        Loads the state. Returns expiry timestamp if valid, else 0.
        Retries up to 3 times to handle potential file locking race conditions.
        """
        if not os.path.exists(STATE_FILE):
            return 0
        
        for _ in range(3):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)
                
                expiry = data.get("expiry", 0)
                signature = data.get("signature", "")

                # Verify signature
                expected_signature = StateManager._calculate_hash(str(expiry))
                if hmac.compare_digest(signature, expected_signature):
                    return expiry
                else:
                    return 0
            except (IOError, json.JSONDecodeError):
                time.sleep(0.1)
                continue
            except Exception:
                return 0
        return 0

    @staticmethod
    def grant_reward(minutes):
        """
        Grants reward time by setting status to NOW + minutes.
        Retries up to 5 times.
        """
        expiry = time.time() + (minutes * 60)
        signature = StateManager._calculate_hash(str(expiry))
        
        data = {
            "expiry": expiry,
            "signature": signature
        }

        for _ in range(5):
            try:
                with open(STATE_FILE, "w") as f:
                    json.dump(data, f)
                return True
            except IOError as e:
                print(f"Error saving state (retrying): {e}")
                time.sleep(0.2)
        
        print("Failed to save state after retries.")
        return False

    @staticmethod
    def is_reward_active():
        """
        Checks if the current time is within the reward period.
        """
        expiry = StateManager.load_state()
        remaining = expiry - time.time()
        return remaining > 0
