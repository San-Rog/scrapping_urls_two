import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.tjma.jus.br/') as resp:
            print(resp.status)
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            texto_limpo = soup.get_text(separator=' ', strip=True)
            print(texto_limpo)

asyncio.run(main())

 
