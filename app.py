import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import filedialog, messagebox
from search import search_articles


root = tk.Tk()
root.title("高校理论文章检索器")
root.configure(bg="white")
root.geometry("400x300")


def get_selected_date():
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
    search_articles(year, month, date, path_label.cget("text"))
    messagebox.showinfo("提示", "检索完成！")

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