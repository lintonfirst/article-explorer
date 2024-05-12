from RMRB import getRMRB
from GMRB import getGMRB
from JFRB import getJFRB
from WHB import getWHB
import openpyxl
import datetime

def search_article_RMRB(year:str,month:str,date:str,ws,ps,stepProgress:callable):
    
    # 人民日报
    results,potentials=getRMRB(year,month,date)
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])   
    
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    stepProgress()

def search_article_GMRB(year:str,month:str,date:str,ws,ps,stepProgress:callable):
    
    # 光明日报
    results,potentials=getGMRB(year,month,date)
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    stepProgress()

def search_article_JFRB(year:str,month:str,date:str,ws,ps,stepProgress:callable):
    # 解放日报
    results,potentials=getJFRB(year,month,date)
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    stepProgress()

def search_article_WHB(year:str,month:str,date:str,ws,ps,stepProgress:callable):
    # 文汇报
    results,potentials=getWHB(year,month,date)
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    stepProgress()
    
    
