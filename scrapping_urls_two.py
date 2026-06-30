import aiohttp
import asyncio
import streamlit as st
from bs4 import BeautifulSoup

async def main(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            texto_limpo = soup.get_text(separator=' ', strip=True)
            st.write(texto_limpo)

asyncio.run(main('http://www.tjma.jus.br/'))

 
