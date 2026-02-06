import aiosqlite
    
async def sql3_table() -> None:
    async with aiosqlite.connect('Addresses.sqlite') as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('CREATE TABLE IF NOT EXISTS Clients ('
                            'client_id BIGINT, '
                            'row TEXT)'
                            )
        finally:
            if csr != None:
                await csr.close()
            
    
async def sql3_remove_row(client, row) -> None:
    async with aiosqlite.connect('Addresses.sqlite', isolation_level=None) as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('DELETE FROM Multichain Clients '
                            'WHERE client_id = ? '
                            'AND row = ?', 
                            (client, row)
                            )
        finally:
            if csr != None:
                await csr.close()
            
async def sql3_receipt_row(client) -> None:
    async with aiosqlite.connect('Addresses.sqlite', isolation_level=None) as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('SELECT * FROM Clients '
                                'WHERE client_id = ?',
                                (client, )
                                )
            
            data = await csr.fetchall()
            return data
        finally:
            if csr != None:
                await csr.close()
        
async def sql3_addopt_row(client, row) -> None:
    async with aiosqlite.connect('Addresses.sqlite', isolation_level=None) as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('INSERT INTO Clients '
                            '(client_id, row) '
                            'VALUES (?, ?)',
                            (client, row)
                            )
        finally:
            if csr != None:
                await csr.close()
