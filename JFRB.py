# 爬取解放日报
import requests
import threading

def getArticles_V1(year:str,month:str,date:str):
    url="https://www.jfdaily.com/staticsg/data/journal/"+year+"-"+month+"-"+date+"/navi.json"
    jsonDatas=requests.get(url).json()
    pages=jsonDatas['pages']
    articleLists=[]
    for page in pages:
        pageName=page['pnumber']+"版："+page['pname']
        for article in page['articleList']:
            id=article['id']
            author=article['author']
            url="https://www.jfdaily.com/staticsg/res/html/journal/detail.html?date={}&id={}&page={}".format(year+"-"+month+"-"+date,id,page['pnumber'])
            jsonUrl="https://www.jfdaily.com/staticsg/data/journal/{}/{}/article/{}.json".format(year+"-"+month+"-"+date,page['pnumber'],id)
            articleLists.append({"title":article['title'],"url":url,"date":year+"-"+month+"-"+date,"page":pageName,"source":"解放日报","author":author,"jsonUrl":jsonUrl})
    return articleLists

def getAricleDetail_V1(data):
    url=data['jsonUrl']
    jsonDatas=requests.get(url).json()
    article=jsonDatas['article']
    content=article['content']
    paragraphs=content.split("<br/>")
    textLength=0
    count=0
    for p in paragraphs:
        textLength+=len(p)
        if p.find('（作者为')!=-1:
            unit=p[p.find('（作者为')+4:-1]
            if unit.find('大学')!=-1 or unit.find('学院')!=-1 or unit.find("党校")!=-1:
                data['unit']=unit
                count+=1
    data['textLength']=textLength
    if count==1:
        return data,1
    if count>1:
        return data,count
    return None,0

def getJFRB_V1(year:str,month:str,date:str): #2024年12月15日前的版本
    lists=getArticles_V1(year,month,date)
    results=[]
    potentials=[]
    threads=[]
    def task(article):
        try:
            res,count=getAricleDetail_V1(article)
            if count==1:
                results.append(res)
            if count>1:
                potentials.append(res)
        except:
            pass
    for article in lists:
        t=threading.Thread(target=task,args=(article,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results,potentials

def getArticles_V2(year:str,month:str,date:str):
    url="https://www.jfdaily.com/journal/"+year+"-"+month+"-"+date+"/getJournalPage.do"
    jsonDatas=requests.get(url).json()
    pages=jsonDatas['object']['pagelist']
    articleLists=[]
    threads=[]
    def task(page):
        try:
            pageName=page['pnumber']+"版："+page['pname']
            pageUrl=url+"?page="+page['pnumber']
            pageData=requests.get(pageUrl).json()
            for article in pageData['object']['articlelist']:
                id=article['id']
                articleUrl="https://www.jfdaily.com/staticsg/res/html/journal/detail.html?date={}&id={}&page={}".format(year+"-"+month+"-"+date,id,page['pnumber'])
                jsonUrl="https://www.jfdaily.com/journal/getJournalPageArticle.do?id={}".format(id)
                author=requests.get(jsonUrl).json()['object']['article']['author']
                articleLists.append({"title":article['title'],"url":articleUrl,"date":year+"-"+month+"-"+date,"page":pageName,"source":"解放日报","author":author,"jsonUrl":jsonUrl})
        except:
            pass
    for page in pages:
        t=threading.Thread(target=task,args=(page,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
       
    return articleLists

def getAricleDetail_V2(data):
    url=data['jsonUrl']
    jsonDatas=requests.get(url).json()
    article=jsonDatas['object']['article']
    content=article['content']
    paragraphs=content.split("<br/>")
    textLength=0
    count=0
    for p in paragraphs:
        textLength+=len(p)
        if p.find('（作者为')!=-1:
            unit=p[p.find('（作者为')+4:-1]
            if unit.find('大学')!=-1 or unit.find('学院')!=-1 or unit.find("党校")!=-1:
                data['unit']=unit
                count+=1
    data['textLength']=textLength
    if count==1:
        return data,1
    if count>1:
        return data,count
    return None,0

def getJFRB_V2(year:str,month:str,date:str): #2024年12月16日后的版本
    lists=getArticles_V2(year,month,date)
    results=[]
    potentials=[]
    threads=[]
    def task(article):
        try:
            res,count=getAricleDetail_V2(article)
            if count==1:
                results.append(res)
            if count>1:
                potentials.append(res)
        except:
            pass
    for article in lists:
        t=threading.Thread(target=task,args=(article,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results,potentials

def getJFRB(year:str,month:str,date:str):
    url="https://www.jfdaily.com/staticsg/data/journal/"+year+"-"+month+"-"+date+"/navi.json"
    if requests.get(url).status_code==200:
        return getJFRB_V1(year,month,date)
    else:
        return getJFRB_V2(year,month,date)
