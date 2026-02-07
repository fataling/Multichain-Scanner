from .exceptions import (
    InvalidBinaryData, 
    InvalidTypeData, 
    InvalidTypeString, 
    NotChecksumString, 
    NotCorrectString
)

from eth_utils import (
    is_checksum_address,
    is_address,
    is_hex_address,
    is_binary_address,
    is_normalized_address
)

def validate_eth(data : str):
    if not isinstance(data, str):
        raise InvalidTypeData(
            f'Address is not string, chech his'
        )
    
    if not is_hex_address(data):
        raise InvalidTypeString(
            f'Address {data} must start with 0x, resend your string'
        )

    if not is_binary_address(data):
        raise InvalidBinaryData(
            f'Address {data} not binary'
        )

    # if not is_normalized_address(data):
    #     raise ValidationError(
    #         f'This address is not ens'
    #     )
        
    if not is_checksum_address(data):
        raise NotChecksumString(
            f'Address is not checksumed'
        )
    
    if not is_address(data):
        raise NotCorrectString(
            f'String {data} is not address'
        )
