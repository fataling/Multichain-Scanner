import aiosqlite
    
async def sql3_table() -> None:
    async with aiosqlite.connect('Addresses.sqlite') as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('CREATE TABLE IF NOT EXISTS Clients ('
                              'client_id BIGINT, '
                              'row TEXT) '
                              )
        finally:
            if csr != None:
                await csr.close()
            
async def sql3_remove_row(client: int, row: str) -> None:
    async with aiosqlite.connect('Addresses.sqlite') as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('DELETE FROM Clients WHERE client_id = ? AND row = ? ',
                             (client, row)
                             )
            await cnn.commit()
        finally:
            if csr != None:
                await csr.close()
                
async def sql3_remove_all_row(client: int) -> None:
    async with aiosqlite.connect('Addresses.sqlite') as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('DELETE FROM Clients WHERE client_id = ? ',
                             (client, )
                             )
            await cnn.commit()
        finally:
            if csr != None:
                await csr.close()
                
async def sql3_receipt_row(client: int) -> str | None:
    async with aiosqlite.connect('Addresses.sqlite') as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('SELECT row FROM Clients '
                              'WHERE client_id = ? '
                              'LIMIT 5',
                              (client, )
                              )
            
            raw_data = await csr.fetchall()
            
            if raw_data != []:
                rows = [row[0] for row in raw_data]
                return rows
            return None
        finally:
            if csr != None:
                await csr.close()
    
async def sql3_addopt_row(client: int, row: str) -> None:
    async with aiosqlite.connect('Addresses.sqlite') as cnn:
        try:
            csr = await cnn.cursor()
            
            await csr.execute('INSERT INTO Clients '
                              '(client_id, row) '
                              'VALUES (?, ?)',
                              (client, row)
                              )
            await cnn.commit()
        finally:
            if csr != None:
                await csr.close()
