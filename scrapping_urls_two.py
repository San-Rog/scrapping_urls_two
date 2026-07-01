import aiohttp
import asyncio
import requests
import os
import streamlit as st
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class acessories():
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
    
    def validate(self):
        try:
            parsed = urlparse(self.url)
            return all([parsed.scheme, parsed.netloc])
        except ValueError:
            return False
      
    def textUrl(self):
        allText = []
        fileSoup = self.soup.find_all("a", href=True)
        for file in fileSoup:
            href = file['href']
            objAcessories = acessories(None, href)
            if objAcessories.validate():  
                allText.append(href)
        return allText
    
class extractElems():
    def __init__(self, *args):    
        self.soup = args[0]
        self.url = args[1]
        
    def extractText(self):
        with st.spinner(text='Scrapping do texto do site {self.url}...', show_time=True, width="stretch"):
            textClear = self.soup.get_text(separator='\n', strip=True)
            st.write(textClear)
        return textClear

    def extractLinks(self): 
        objAcessories = acessories(self.soup, self.url)
        with st.spinner(text='Scrapping dos links do site {self.url}...', show_time=True, width="stretch"):
            links = objAcessories.textUrl()
            for link in links:
                st.write(link)
        return links
           
    def extracImgs(self):
        with st.spinner(text='Scrapping das imagens do site {self.url}...', show_time=True, width="stretch"):
            imagens = self.soup.find_all('img')
            roleUrls = []
            for img in imagens:
                link = img.get('src')
                if link:
                    linkFull = urljoin(self.url, link)
                    roleUrls.append(linkFull)
            st.write(roleUrls)
            roleUrls = [imgUrl for imgUrl in list(set(roleUrls)) if len(imgUrl)]
            roleImg = [imgUrl.replace(self.url, '').strip() for imgUrl in roleUrls]
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
        return roleUrls
    
    def extractFiles(self): 
        objAcessories = acessories(self.soup, self.url)
        with st.spinner(text='Scrapping dos links do site {self.url}...', show_time=True, width="stretch"):
            files = [file for file in objAcessories.textUrl() if os.path.splitext(file)[1].strip() != '']
            for file in files:
                st.write(file)
        return files        

class operations():
    def __init__(self, *args):    
        self.url = args[0]

    async def scrap(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
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
        objOperation = operations(self.urlBase)
        self.soup = asyncio.run(objOperation.scrap())
        if len(self.soup) > 0:
            objExtract = extractElems(self.soup, self.urlBase)
            self.allText = objExtract.extractText()
            self.allLinks = objExtract.extractLinks()
            self.allImgs = objExtract.extracImgs()
            self.allFiles = objExtract.extractFiles()
    
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


 
