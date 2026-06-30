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
 
def extratText(soup, url):
    with st.spinner(text='Scrapping do texto do site {url}...', show_time=True, width="stretch"):
        textClear = soup.get_text(separator='\n', strip=True)
        st.write(textClear)
 
def extractLinks(soup, url): 
    with st.spinner(text='Scrapping dos links do site {url}...', show_time=True, width="stretch"):
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if validate(href):  
                st.write(href, len(href))

def extracImgs(soup, url):
    with st.spinner(text='Scrapping das imagens do site {url}...', show_time=True, width="stretch"):
        imagens = soup.find_all('img')
        roleUrls = []
        for img in imagens:
            link = img.get('src')
            if link:
                linkFull = urljoin(url, link)
                roleUrls.append(linkFull)
            roleUrls = [imgUrl for imgUrl in list(set(roleUrls)) if len(imgUrl) > 0)]
            if roleUrls:
                colunas = st.columns(3) 
                for i, imgUrl in enumerate(roleUrls):
                    st.write(imgUrl)
                    #col = colunas[i % 3]
                    #with col:
                    #    st.image(imgUrl, caption=f"Imagem {i+1}", use_column_width=True)
            else:
                st.info("Nenhuma imagem foi encontrada nesta página.")

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
    soup = asyncio.run(scrap(urlBase))
    if len(soup) > 0:
        extratText(soup, urlBase)
        extractLinks(soup, urlBase)
        extracImgs(soup, urlBase)

if __name__ == '__main__':
    main()

#https://scrappingurlstwo-aouanptf499cdt98bpmjvg.streamlit.app/
#https://docs.aiohttp.org/en/stable/client_quickstart.html


 
