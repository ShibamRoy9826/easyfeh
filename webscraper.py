import toml
from requests import get
from conf import *
from bs4 import BeautifulSoup
from re import sub
from string import ascii_letters
from random import shuffle

with open(config_path, "r") as f:
    config = toml.load(f)

class Downloader:
    def __init__(self,query,source=0):
        global config
        query=self.formatQuery(query)
        self.images=[]
        self.download_dir=config["internet"]["wallpaper_save_directory"]
        # Source 0 -> unsplash(default)
        # Source 1 -> To be added later 
        if source==1:
            self.source=""
            self.source_num=1
        else:
            self.source=f"https://unsplash.com/s/photos/{query}"
            self.source_num=0

    def formatQuery(self,query):
        q=sub(r'\s+',' ',query).strip()
        q.replace(' ','-')
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
    def getRandom(self,count=1):
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
            return [] # to be added later

    def downloadRandom(self,count=1):
        a=self.getRandom(count=count)
        for img in a:
            self.downloadImage(img[0],img[1])
            self.images.append(img[1])


