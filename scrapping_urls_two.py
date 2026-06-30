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
            texto_limpo = soup.get_text(separator='\n', strip=True)
            st.write(texto_limpo)
            links = [link.get('href') for link soup.find_all('a') if href]
            st.write(links)

asyncio.run(main('http://www.tjma.jus.br/'))

