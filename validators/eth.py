from eth_utils import (
    is_checksum_address,
    is_address,
    is_hex_address
)

from typing import Optional

def valid_string_eth(data: str) -> Optional[bool]:
    if not isinstance(data, str):
        return False
    
    if not is_hex_address(data):
        return False
    
    if not is_address(data):
        return False

    if not is_checksum_address(data):
        return False
    
    return True
