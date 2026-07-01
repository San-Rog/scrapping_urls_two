import aiohttp
import asyncio
import mimetypes
import os
import zipfile
import io
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
        
    def urlIsFile(self):
        parsed_url = urlparse(self.url)
        mime_type, _ = mimetypes.guess_type(parsed_url.path)
        if mime_type and 'text/html' not in mime_type:
            return True
        return False
            
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
            newFiles = []
            for file in files:
                objAcessories = acessories(None, file)
                if objAcessories.urlIsFile():
                    newFiles.append(file)
        return newFiles 

class downloads(): 
    def __init__(self, arguments):   
        self.urls, self.textSpin, self.textDown, self.nameDown = arguments
    
    def downFiles(self): 
        objOperation = operations(None, self.urls, None)
        with st.spinner(self.textSpin):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            imagens_bytes = loop.run_until_complete(objOperation.downAll())
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, img in enumerate(imagens_bytes):
                if img:
                    zip_file.writestr(os.path.basename(self.urls[i]), img)
        zip_data = zip_buffer.getvalue()
        st.download_button(
            label=f"📥 {self.textDown}",
            data=zip_data,
            file_name=self.nameDown,
            mime="application/zip"
        )
        st.success("Download concluído! Clique no botão acima para salvar.")

class operations():
    def __init__(self, *args):    
        self.url = args[0]
        self.urls = args[1]
        self.session = args[2]
    
    async def scrap(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                try:
                    htmlText = await resp.text()
                    soup = BeautifulSoup(htmlText, 'html.parser')   
                    return soup
                except:
                    return ''
                    
    async def downImg(self):
        try:
            async with self.session.get(self.url) as response:
                if response.status == 200:
                    return await response.read()
        except Exception as error:
            filesFail.append(self.url)
            st.markdown(self.url, unsafe_allow_html=True, width="stretch", 
                        text_alignment="left")
        return None

    async def downAll(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                objOperation = operations(url, None, session)
                tasks.append(objOperation.downImg())
            return await asyncio.gather(*tasks)
              
class main():
    def __init__(self):
        global filesFail
        filesFail = []
        self.setPage() 
        urlBase = "https://www.tjma.jus.br/"
        objOperation = operations(urlBase, None, None)
        soup = asyncio.run(objOperation.scrap())
        if len(soup) > 0:
            objExtract = extractElems(soup, urlBase)
            allText = objExtract.extractText()
            allLinks = objExtract.extractLinks()
            allImgs = objExtract.extracImgs()
            allFiles = objExtract.extractFiles()
            arguments = []
            if st.button("Download imagens"):
                st.write(allImgs)
                arguments = [allImgs, "Baixar imagens...", "Baixar todas as imagens (ZIP)", "imagens_scraping.zip"]
            if st.button("Download arquivos"):
                st.write(allFiles)
                arguments = [allFiles, "Baixar arquivos...", "Baixar todos os arquivos (ZIP)", "arquivos_scraping.zip"]
            if len(arguments):
                objDown = downloads(arguments)
                objDown.downFiles() 
            if len(filesFail) > 0:
                for file in filesFail:
                    fileHtml = f"""
                        <meta http-equiv="refresh" content="0; url={file}">
                    """
                    st.markdown(fileHtml, unsafe_allow_html=True)
 
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


 
