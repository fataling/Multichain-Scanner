from eth_utils import (
    is_checksum_address,
    is_address,
    is_hex_address
)

def valid_string_evm(data: str):
    if not isinstance(data, str):
        raise ValueError(
            f'Address is not string, chech his'
        )
    
    if not is_hex_address(data):
        raise ValueError(
            f'Address {data} must start with 0x, resend your string'
        )
    
    if not is_address(data):
        raise ValueError(
            f'String {data} is not address'
        )

    if not is_checksum_address(data):
        raise ValueError(
            f'Address is not checksumed'
        )
        
