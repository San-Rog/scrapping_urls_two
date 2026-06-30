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
        texto_limpo = soup.get_text(separator='\n', strip=True)
        st.write(texto_limpo)
 
def extractLinks(soup, url): 
    with st.spinner(text='Scrapping dos links do site {url}...', show_time=True, width="stretch"):
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if validate(href):  
                st.write(href, len(href))

def extracImgs(soup, url):
    with st.spinner(text='Scrapping dos links do site {url}...', show_time=True, width="stretch"):
        imagens = soup.find_all('img')
        lista_urls = []
        for img in imagens:
            link = img.get('src')
            if link:
                link_completo = urljoin(url, link)
                lista_urls.append(link_completo)
            lista_urls = list(set(lista_urls))
            if lista_urls:
                colunas = st.columns(3) 
                for i, img_url in enumerate(lista_urls):
                    col = colunas[i % 3]
                    with col:
                        st.image(img_url, caption=f"Imagem {i+1}", use_column_width=True)
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


 


 


 
