from requests import get
from .conf import *
from bs4 import BeautifulSoup
from re import sub
from string import ascii_letters
from random import shuffle
from rich.console import Console

with open(config_path, "r") as f:
    config = load(f)

class Downloader:
    def __init__(self,query,source=1):
        global config
        self.c=Console()
        self.q=self.formatQuery(query)
        self.images=[]
        self.download_dir=config["internet"]["wallpaper_save_directory"]
        # Source 0 -> unsplash
        # Source 1 -> wallhaven (default)
        if source==1:
            wallhaven_query=self.formatQuery(query,separator="+")
            if config["internet"]["wallhaven_purity"]=="sfw":
                self.purity_level="100"
            else:
                self.purity_level="000"
            self.source=f"https://wallhaven.cc/search?q={wallhaven_query}&categories=110&purity={self.purity_level}&sorting=random&order=desc&ai_art_filter=1"
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
            if config["internet"]["use_api"]:
                if config["internet"]["wallhaven_api_key"]=="":
                    p={
                        "q":config["internet"]["image_query"],
                        "categories":"111",
                        "purity":"100",
                        "sorting":"random"
                    }

                    if config["internet"]["wallhaven_purity"]!="sfw":
                        self.c.print("[red]Error:[/red] You either need to set your API key, or use sfw images from wallhaven...")
                        

                    r=get("https://wallhaven.cc/api/v1/search",params=p)
                    rjson=r.json()
                    for item in rjson["data"]:
                        imgAddr=item["path"]
                        flname=self.download_dir+"/"+imgAddr[imgAddr.rfind('/')+1:]
                        toAdd=[imgAddr,flname]
                        results.append(toAdd)
                else:
                    p={
                        "q":config["internet"]["image_query"],
                        "categories":"111",
                        "purity": self.purity_level,
                        "sorting":"random",
                        "api_key":config["internet"]["wallhaven_api_key"]
                    }

                    if config["internet"]["wallhaven_purity"]!="sfw":
                        self.c.print("[red]Error:[/red] You either need to set your API key, or use sfw images from wallhaven...")
                        

                    r=get("https://wallhaven.cc/api/v1/search",params=p)
                    rjson=r.json()
                    for item in rjson["data"]:
                        imgAddr=item["path"]
                        flname=self.download_dir+"/"+imgAddr[imgAddr.rfind('/')+1:]
                        toAdd=[imgAddr,flname]
                        results.append(toAdd)

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


