import aiohttp
import asyncio
import streamlit as st
from urllib.parse import urljoin, urlparse
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

def extracImgs(soup):
    pass

async def scrap(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                htmlText = await resp.text()
                soup = BeautifulSoup(htmlText, 'html.parser')   
                return soup
            except:
                return ''
                
def main():
    urlBase = "http://www.tjma.jus.br/"
    soup = asyncio.run(scrap(urlBase)
    if len(soup) > 0:
        extratText(soup)
        extractLinks(soup)
        extracImgs(soup)

if __name__ == '__main__':
    main()

#https://scrappingurlstwo-aouanptf499cdt98bpmjvg.streamlit.app/
#https://docs.aiohttp.org/en/stable/client_quickstart.html

 
