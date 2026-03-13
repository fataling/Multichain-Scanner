from pytoniq_core import Address, AddressError

from typing import Optional

def valid_string_ton(data: str) -> Optional[bool]:
    if not isinstance(data, str):
        return False
    try:
        if not Address(data):
            raise AddressError
    except:
        return False
    return True
