import aiohttp
import asyncio
import streamlit as st
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def validate(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except ValueError:
        return False
 
def extratText(soup):
    texto_limpo = soup.get_text(separator='\n', strip=True)
    st.write(texto_limpo)
 
def extractLinks(soup): 
    for link in soup.find_all('a'):
        href = link.get('href')
        if validate(href):  
            st.write(href, len(href))

async def main(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                htmlText = await resp.text()
                soup = BeautifulSoup(htmlText, 'html.parser')   
                return soup
            except:
                return ''

soup = asyncio.run(main('http://www.tjma.jus.br/'))
if len(soup) > 0:
    extratText(soup)
    extractLinks(soup)

#https://scrappingurlstwo-aouanptf499cdt98bpmjvg.streamlit.app/

 
