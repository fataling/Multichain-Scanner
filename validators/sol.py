from solders.pubkey import Pubkey

from typing import Optional

def valid_string_sol(data: str) -> Optional[bool]:
    try:
        if not Pubkey.from_string(data):
            return False
    except:
        return False    
    return True
