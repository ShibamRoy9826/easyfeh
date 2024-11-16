import toml
from requests import get
from .conf import *
from bs4 import BeautifulSoup
from re import sub
from string import ascii_letters
from random import shuffle

with open(config_path, "r") as f:
    config = toml.load(f)

class Downloader:
    def __init__(self,query,source=0):
        global config
        self.q=self.formatQuery(query)
        self.images=[]
        self.download_dir=config["internet"]["wallpaper_save_directory"]
        # Source 0 -> unsplash(default)
        # Source 1 -> wallhaven
        if source==1:
            wallhaven_query=self.formatQuery(query,separator="+")
            if config["internet"]["wallhaven_purity"]=="sfw":
                purity_level="100"
            else:
                purity_level="000"
            self.source=f"https://wallhaven.cc/search?q={wallhaven_query}&categories=110&purity={purity_level}&sorting=random&order=desc&ai_art_filter=1"
            self.source_num=1
        else:
            self.source=f"https://unsplash.com/s/photos/{query}"
            self.source_num=0

    def formatQuery(self,query,separator="-"):
        q=sub(r'\s+',' ',query).strip()
        q.replace(' ',separator)
        return q
    def downloadImage(self,url,downloadPath):
        res=get(url)
        if res.status_code==200:
            with open(downloadPath,"wb") as f:
                f.write(res.content)
    def generateName(self,chars):
        lst=[]
        for i in ascii_letters:
            lst.append(i)
        shuffle(lst)
        name=""
        for i in lst[:chars]:
            name+=i
        return name
    def search(self,count=1):
        res=get(self.source)
        htmldata = res.text
        soup = BeautifulSoup(htmldata, 'html.parser')  
        results=[]
        if self.source_num==0:
            for item in soup.find_all('img'): 
                imgAddr=item['src']
                if imgAddr.startswith("https://images.unsplash.com/photo"):
                    n=self.generateName(10)
                    flname=self.download_dir+f"/{n}.jpg"
                    results.append([imgAddr,flname])
            if config["internet"]["shuffle_results"] ==True:
                shuffle(results)
            return results[:count]
        else:
            images=[]
            cnt=0
            for item in soup.find_all('a'):
                if item!=None:
                    try:
                        if item.get("href").startswith("https://wallhaven.cc/w/"):
                            images.append(item.get("href"))
                            cnt+=1
                            if cnt==count:
                                break
                    except:
                        pass
            for img in images:
                r=get(img)
                html=r.text
                s=BeautifulSoup(html,"html.parser")
                img=s.find(id="wallpaper")
                if img!=None:
                    imgAddr=img.get('src')
                    flname=self.download_dir+"/"+imgAddr[imgAddr.rfind('/')+1:]
                    results.append([imgAddr,flname])
            return results


    def download(self,count=1):
        a=self.search(count=count)
        for img in a:
            self.downloadImage(img[0],img[1])
            self.images.append(img[1])


