from RMRB import getRMRB
import openpyxl

def search(year:str,month:str,date:str):
    results,potentials=getRMRB(year,month,date)
    wb=openpyxl.Workbook()
    wb.remove(wb.active)
    ws=wb.create_sheet("人民日报")
    ws.append(["报刊名","日期","具体版面","文章名称","作者","具体所属单位","字数","链接"])
    for res in results:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['author'].strip(),res['unit'].strip(),res['textLength'],res['url'].strip()])
    
    ws=wb.create_sheet("潜在文章")
    ws.append(["报刊名","日期","具体版面","文章名称""链接"])
    for res in potentials:
        ws.append([res['source'].strip(),res['date'].strip(),res['page'].strip(),res['title'].strip(),res['url'].strip()])
