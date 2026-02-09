from solders.pubkey import Pubkey

def valid_string_sol(data: str):
    if not Pubkey.from_string(data):
        raise ValueError(
            f'This addres is invalid'
        )
