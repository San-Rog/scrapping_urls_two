import aiohttp
import asyncio
import streamlit as st
from bs4 import BeautifulSoup

async def main(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            st.write(resp.status)
            htmlText = await resp.text()
            soup = BeautifulSoup(htmlText , 'html.parser')
            texto_limpo = soup.get_text(separator=' ', strip=True)
            st.write(texto_limpo)

asyncio.run(main('http://www.tjma.jus.br/'))

 
