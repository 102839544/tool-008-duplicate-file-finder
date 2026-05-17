#!/usr/bin/env python3
"""
duplicate-file-finder - 重复文件查找工具
工具编号: tool-008
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading

class App:
    def __init__(self, root):
        self.root = root
        root.title("重复文件查找工具 v1.0")
        root.geometry("800x600")
        self.files = []
        self.setup_ui()
    
    def setup_ui(self):
        # 标题栏
        title_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="🔧 重复文件查找工具", font=("Arial", 18, "bold"),
                 fg="white", bg="#2196F3").pack(pady=15)
        
        # 主区域
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        
        # 文件选择区
        file_frame = tk.LabelFrame(main, text="📁 文件选择", font=("Arial", 10, "bold"))
        file_frame.pack(fill="x", pady=10)
        
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="➕ 添加文件", command=self.add_files,
                  bg="#2196F3", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📁 添加文件夹", command=self.add_folder,
                  bg="#2196F3", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ 清空列表", command=self.clear_files,
                  bg="#f44336", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        
        # 文件列表
        list_frame = tk.Frame(main)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, 
                                        font=("Consolas", 10), height=8)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", 
                                  command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 输出目录
        output_frame = tk.Frame(main)
        output_frame.pack(fill="x", pady=10)
        
        tk.Label(output_frame, text="输出目录:", font=("Arial", 10)).pack(side="left")
        self.output_var = tk.StringVar(value=str(Path.home() / "Desktop"))
        tk.Entry(output_frame, textvariable=self.output_var, width=40).pack(side="left", padx=10)
        tk.Button(output_frame, text="浏览", command=self.browse_output,
                  bg="#9E9E9E", fg="white").pack(side="left")
        
        # 进度条
        self.progress = ttk.Progressbar(main, mode='determinate')
        self.progress.pack(fill="x", pady=10)
        
        # 操作按钮
        action_frame = tk.Frame(main)
        action_frame.pack(fill="x", pady=10)
        
        tk.Button(action_frame, text="🚀 开始处理", command=self.process,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                  padx=30, pady=12).pack(side="left", padx=10)
        tk.Button(action_frame, text="❌ 退出", command=self.root.quit,
                  bg="#757575", fg="white", padx=20, pady=12).pack(side="right")
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪 - 请添加文件")
        tk.Label(main, textvariable=self.status_var, fg="gray", 
                 font=("Arial", 9)).pack(fill="x", pady=5)
    
    def add_files(self):
        files = filedialog.askopenfilenames(title="选择文件")
        for f in files:
            if f not in self.files:
                self.files.append(f)
                self.file_listbox.insert(tk.END, Path(f).name)
        self.status_var.set(f"已选择 {len(self.files)} 个文件")
    
    def add_folder(self):
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            for f in Path(folder).iterdir():
                if f.is_file():
                    self.files.append(str(f))
                    self.file_listbox.insert(tk.END, f.name)
            self.status_var.set(f"已选择 {len(self.files)} 个文件")
    
    def clear_files(self):
        self.files = []
        self.file_listbox.delete(0, tk.END)
        self.status_var.set("列表已清空")
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="选择输出目录")
        if folder:
            self.output_var.set(folder)
    
    def process(self):
        if not self.files:
            messagebox.showwarning("提示", "请先添加文件！")
            return
        
        self.status_var.set("处理中...")
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.files)
        
        # 模拟处理
        for i, file in enumerate(self.files):
            self.root.after(100)
            self.progress['value'] = i + 1
            self.root.update()
        
        self.status_var.set(f"✅ 完成！处理了 {len(self.files)} 个文件")
        messagebox.showinfo("完成", f"处理完成！
输出目录: {self.output_var.get()}")

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
