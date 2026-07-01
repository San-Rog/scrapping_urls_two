import aiohttp
import asyncio
import streamlit as st
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class acessories():
    def __init__(self):    
        pass
    
    def validate(self, url):
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except ValueError:
            return False
      
    def textUrl(_self, soup, url):
        allText = []
        fileSoup = soup.find_all("a", href=True)
        for file in fileSoup:
            href = file['href']
            if validate(href):  
                allText.append(href)
        return allText
    
class extractElems():
    def __init__(self):    
        pass
    
    def extractText(self, soup, url):
        with st.spinner(text='Scrapping do texto do site {url}...', show_time=True, width="stretch"):
            textClear = soup.get_text(separator='\n', strip=True)
            st.write(textClear)

    def extractLinks(self, soup, url): 
        with st.spinner(text='Scrapping dos links do site {url}...', show_time=True, width="stretch"):
            links = textUrl(soup, url)
            for link in links:
                st.write(link)
           
    def extracImgs(self, soup, url):
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


    def extractFiles(self, soup, url): 
        with st.spinner(text='Scrapping dos links do site {url}...', show_time=True, width="stretch"):
            links = textUrl(soup, url)
            for link in links:
                st.write(link)

async def scrap(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                htmlText = await resp.text()
                soup = BeautifulSoup(htmlText, 'html.parser')   
                return soup
            except:
                return ''
                
class main():
    def __init__(self):
        self.setPage() 
        self.urlBase = "https://ww2.trt2.jus.br/"
        self.soup = asyncio.run(scrap(urlBase))
        if len(self.soup) > 0:
            objExtract = extractElem
            objExtract.extractText(self.soup, urlBase)
            objExtract.extractLinks(self.soup, urlBase)
            objExtract.extracImgs(self.soup, urlBase)
            objExtract.extractFiles(self.soup, urlBase)
    
    def setPage(self):
        st.set_page_config(
            page_title='Mescla de imagens',
            page_icon=':material/image:',
            layout='wide', 
            initial_sidebar_state=None, 
            menu_items=None) 

if __name__ == '__main__':
    main()

#https://scrappingurlstwo-aouanptf499cdt98bpmjvg.streamlit.app/
#https://docs.aiohttp.org/en/stable/client_quickstart.html


 
