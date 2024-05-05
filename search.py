from RMRB import getRMRB
from GMRB import getGMRB
from JFRB import getJFRB
from WHB import getWHB
import openpyxl
import datetime

def search_articles(year:str,month:str,date:str,path:str):
    
    # 人民日报
    results,potentials=getRMRB(year,month,date)
    wb=openpyxl.Workbook()
    wb.remove(wb.active)
    ws=wb.create_sheet("人民日报")
    ws.append(["报刊名","日期","具体版面","文章名称","作者","具体所属单位","字数","链接"])
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    
    ps=wb.create_sheet("潜在文章")
    ps.append(["报刊名","日期","具体版面","文章名称""链接"])
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    
    # 光明日报
    results,potentials=getGMRB(year,month,date)
    ws=wb.create_sheet("光明日报")
    ws.append(["报刊名","日期","具体版面","文章名称","作者","具体所属单位","字数","链接"])
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    
    # 解放日报
    results,potentials=getJFRB(year,month,date)
    ws=wb.create_sheet("解放日报")
    ws.append(["报刊名","日期","具体版面","文章名称","作者","具体所属单位","字数","链接"])
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    
    # 文汇报
    results,potentials=getWHB(year,month,date)
    ws=wb.create_sheet("文汇报")
    ws.append(["报刊名","日期","具体版面","文章名称","作者","具体所属单位","字数","链接"])
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    for res in potentials:
        ps.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
    
    timestamp=datetime.datetime.now().timestamp()
    wb.save(path+"/高校理论文章检索结果{}-{}-{}-{}.xlsx".format(year,month,date,timestamp))
