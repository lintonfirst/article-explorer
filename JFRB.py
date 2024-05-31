# 爬取解放日报
import requests
import threading

def getArticles(year:str,month:str,date:str):
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

def getAricleDetail(data):
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
    

def getJFRB(year:str,month:str,date:str):
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
        t=threading.Thread(target=task,args=(article,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results,potentials