import random
import time
from typing import Dict, Tuple

class OTPManager:
    def __init__(self, expiry_seconds: int = 300):
        self.expiry_seconds = expiry_seconds
        # Stores email -> (otp_code, expiry_timestamp)
        self.otp_cache: Dict[str, Tuple[str, float]] = {}

    def generate_otp(self, email: str) -> str:
        otp = f"{random.randint(100000, 999999)}"
        expiry = time.time() + self.expiry_seconds
        self.otp_cache[email] = (otp, expiry)
        return otp

    def verify_otp(self, email: str, otp: str) -> bool:
        if email not in self.otp_cache:
            return False
        
        cached_otp, expiry = self.otp_cache[email]
        if time.time() > expiry:
            del self.otp_cache[email]
            return False
            
        if cached_otp == otp:
            del self.otp_cache[email]
            return True
            
        return False

otp_manager = OTPManager()
