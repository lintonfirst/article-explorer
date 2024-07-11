# 爬取光明日报
import requests
from bs4 import BeautifulSoup
import threading

def getArticles(year:str,month:str,date:str):
    url="http://epaper.gmw.cn/gmrb/html/"+year+"-"+month+"/"+date+"/nbs.D110000gmrb_01.htm"
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html.parser')
    pagesLists=[]
    for page in soup.find_all('a',id='pageLink'):
        pageUrl=page.get('href')
        pageTitle=page.get_text()
        url="http://epaper.gmw.cn/gmrb/html/"+year+"-"+month+"/"+date+"/"+pageUrl
        pagesLists.append({'title':pageTitle,'url':url})

    articleLists=[]
    for page in pagesLists:
        html = requests.get(page['url'])
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'html.parser')
        lists=soup.find('div',id='titleList')
        for article in lists.find_all('a'):
            url="http://epaper.gmw.cn/gmrb/html/"+year+"-"+month+"/"+date+"/"+article.get('href')
            articleLists.append({"title":article.get_text(),"url":url,"date":year+"-"+month+"-"+date,"page":page['title'],"source":"光明日报","author":""})
    return articleLists
    
def getAricleDetail(data):
    url = data['url']
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup=BeautifulSoup(html.text,'html.parser')
    article=soup.find('div',class_='text_c')
    author=article.find('div',class_='lai').find('span').get_text()
    author=author[3:]
    if author:
        data['author']=author
    content=article.find('div',id='articleContent')
    paragraphs=content.find_all('p')
    textLength=0
    count=0
    for p in paragraphs:
        textLength+=len(p.get_text())
        text=p.get_text().strip()
        if text.find('（作者：')!=-1:
            text=text[4:-1]
            if text.find('大学')!=-1 or text.find('学院')!=-1 or text.find('党校')!=-1:
                if text.find('分别系')!=-1:
                    realUnit=text.split('分别系')[1]
                    data['unit']=realUnit
                    count+=1
                elif text.find('均系')!=-1:
                    realUnit=text.split('均系')[1]
                    data['unit']=realUnit
                    count+=1
                elif text.find('，系')!=-1:
                    units=text.split('；')
                    unit=[]
                    for u in units:
                        if u.find('，系')!=-1:
                            realUnit=u.split('，系')[1]
                            unit.append(realUnit)
                    data['unit']='、'.join(unit)
                    count+=1
                elif text.find('，为')!=-1:
                    realUnit=text.split('，为')[1]
                    data['unit']=realUnit
                    count+=1
    
    data['textLength']=textLength
    if count==1:
        return data,1
    if count>1:
        return data,count
    return None,0
    
    



def getGMRB(year:str,month:str,date:str):
    lists=getArticles(year,month,date)
    results=[]
    potentials=[]
    threads=[]
    
    def task(article):
        try:
            res,count=getAricleDetail(article)
            if count==1:
                results.append(res)
            if count>1:
                potentials.append(res)
        except:
            pass
        
    for article in lists:
        thread=threading.Thread(target=task,args=(article,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return results,potentials