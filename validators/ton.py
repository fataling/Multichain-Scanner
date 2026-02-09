from pytoniq_core import Address, AddressError

def valid_string_ton(data: str):
    if not isinstance(data, str):
        raise ValueError(
            f'this type is incorrect'
        )
    
    if not Address(data):
        raise AddressError(
            f'This is invalid'
        )
