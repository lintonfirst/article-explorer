import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import filedialog, messagebox
from search import search_articles
import threading

root = tk.Tk()
root.title("高校理论文章检索器")
root.configure(bg="white")
root.geometry("400x300")
root.resizable(False, False)

isRunning = False

def get_selected_date():
    if isRunning:
        messagebox.showinfo("提示", "正在检索，请稍等！")
        return
    if not cal.get_date():
        messagebox.showinfo("提示", "请选择日期！")
        return
    if not path_label.cget("text"):
        messagebox.showinfo("提示", "请选择路径！")
        return
    selected_date = cal.get_date()
    split_date = selected_date.split("-")
    year = split_date[0]
    month = split_date[1]
    date = split_date[2]
    
    # 进度条窗口
    progress_dialog = tk.Toplevel(root)
    progress_dialog.geometry("300x100")
    # progress_dialog.wait_window()
    progress_dialog.title("检索进度")
    progress_label = tk.Label(progress_dialog, text="正在检索人民日报...")
    progress_label.pack(padx=20, pady=10)
    progress_bar = ttk.Progressbar(progress_dialog, orient="horizontal", length=200)
    progress_bar.pack(padx=20, pady=10)

    def stepProgress():
        progress_bar["value"] += 25
        if progress_bar["value"] == 25:
            progress_label.config(text="正在检索光明日报...")
        elif progress_bar["value"] == 50:
            progress_label.config(text="正在检索解放日报...")
        elif progress_bar["value"] == 75:
            progress_label.config(text="正在检索文汇报...")
    def run():
        global isRunning
        isRunning = True
        search_articles(year, month, date, path_label.cget("text"), stepProgress)
        isRunning = False
        progress_bar.stop()
        progress_dialog.destroy()
        messagebox.showinfo("提示", "检索完成！")
    calculation_thread = threading.Thread(target=run)
    calculation_thread.start()
    progress_dialog.wait_window()
    

def choose_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        path_label.config(text=directory_path)


cal = Calendar(root, selectmode="day", date_pattern="y-mm-dd")
cal.pack(pady=10)

btn = ttk.Button(root, text="检索指定日期的理论文章", command=get_selected_date)
btn.pack(side="bottom", pady=10)

btn = tk.Button(root, text="选择路径", command=choose_directory)
btn.pack(side="left",padx=10,pady=10)

# 创建标签，用于显示选择的路径
path_label = tk.Label(root, text="")
path_label.pack(side="left",pady=10)

def main():
    root.mainloop()

if __name__ == "__main__":
    main()