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
       
def textUrl(soup, url):
    links = []
    linksAbs = []
    for link in soup.find_all('href', href=True):
        href = link.get('href')
        if validate(href):  
            links.append(href)
            linksAbs.append(urljoin(url, href))
    st.write(links)
    return(links, linksAbs)

def extratText(soup, url):
    with st.spinner(text='Scrapping do texto do site {url}...', show_time=True, width="stretch"):
        textClear = soup.get_text(separator='\n', strip=True)
        st.write(textClear)

def extractLinks(soup, url): 
    with st.spinner(text='Scrapping dos links do site {url}...', show_time=True, width="stretch"):
        links, linksAbs = textUrl(soup, url)
        for link in links:
            st.write(link)
        for linkAb in linksAbs:
            st.write(linkAb)

def extracImgs(soup, url):
    with st.spinner(text='Scrapping das imagens do site {url}...', show_time=True, width="stretch"):
        imagens = soup.find_all('img')
        roleUrls = []
        for img in imagens:
            link = img.get('src')
            if link:
                linkFull = urljoin(url, link)
                roleUrls.append(linkFull)
        st.write(roleUrls)
        roleUrls = [imgUrl for imgUrl in list(set(roleUrls)) if len(imgUrl)]
        roleImg = [imgUrl.replace(url, '').strip() for imgUrl in roleUrls]
        if roleUrls:
            colunas = st.columns(spec=3, gap="small", vertical_alignment="center", border=False, width="stretch") 
            for i, imgUrl in enumerate(roleUrls):
                st.write(imgUrl)
                col = colunas[i % 3]
                with col:
                    colOne, colTwo = st.columns(spec=2, vertical_alignment="center", border=False, width="stretch")
                    colOne.image(imgUrl, use_column_width=True)
                    colTwo.markdown(f"{roleImg[i]} - (imagem {i+1})")
                st.divider()
        else:
            st.info("Nenhuma imagem foi encontrada nesta página.")


def extractFiles(soup, url): 
    with st.spinner(text='Scrapping dos links do site {url}...', show_time=True, width="stretch"):
        links, linksAbs = textUrl(soup, url)
        for link in links:
            st.write(link)
        for linkAb in linksAbs:
            st.write(linkAb)

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
        extractFiles(soup, urlBase)

if __name__ == '__main__':
    st.set_page_config(
        page_title='Mescla de imagens',
        page_icon=':material/image:',
        layout='wide', 
        initial_sidebar_state=None, 
        menu_items=None)    
    main()

#https://scrappingurlstwo-aouanptf499cdt98bpmjvg.streamlit.app/
#https://docs.aiohttp.org/en/stable/client_quickstart.html
