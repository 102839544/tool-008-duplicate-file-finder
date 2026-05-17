#!/usr/bin/env python3
"""
重复文件查找工具 - 查找并删除重复文件
"""
import sys, os, hashlib, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
from collections import defaultdict

class App:
    def __init__(self, root):
        self.root = root
        root.title("重复文件查找工具 v1.0")
        root.geometry("800x600")
        self.duplicates = {}
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#f57c00", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🔍 重复文件查找工具", font=("Arial",14,"bold"),
                 fg="white", bg="#f57c00").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="选择文件夹", command=self.select_folder,
                  bg="#f57c00", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="开始扫描", command=self.scan,
                  bg="#4caf50", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="删除选中", command=self.delete_selected,
                  bg="#d9534f", fg="white", padx=15).pack(side="left", padx=5)
        
        # 进度
        self.progress = tk.ttk.Progressbar(main, mode="determinate")
        self.progress.pack(fill="x", pady=5)
        
        # 结果列表
        self.lb = tk.Listbox(main, font=("Consolas",9), bg="#fff3e0",
                              selectmode="extended", height=20)
        self.lb.pack(fill="both", expand=True, pady=5)
        
        self.status = tk.Label(main, text="选择文件夹开始扫描重复文件",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def select_folder(self):
        self.folder = filedialog.askdirectory(title="选择要扫描的文件夹")
        if self.folder:
            self.status.config(text=f"已选择：{Path(self.folder).name}")
    
    def get_file_hash(self, file_path, block_size=65536):
        """计算文件MD5哈希值"""
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                hasher.update(block)
        return hasher.hexdigest()
    
    def scan(self):
        if not hasattr(self, "folder"):
            messagebox.showwarning("提示", "请先选择文件夹")
            return
        
        self.lb.delete(0, "end")
        self.duplicates.clear()
        
        # 收集所有文件
        files = list(Path(self.folder).rglob("*"))
        files = [f for f in files if f.is_file()]
        
        self.progress["maximum"] = len(files)
        
        # 按大小分组
        size_groups = defaultdict(list)
        for i, f in enumerate(files):
            size_groups[f.stat().st_size].append(f)
            self.progress["value"] = i + 1
            self.root.update()
        
        # 只对相同大小的文件计算哈希
        hash_groups = defaultdict(list)
        for size, file_list in size_groups.items():
            if len(file_list) > 1:
                for f in file_list:
                    try:
                        h = self.get_file_hash(f)
                        hash_groups[h].append(f)
                    except:
                        pass
        
        # 找出重复文件
        dup_count = 0
        for h, file_list in hash_groups.items():
            if len(file_list) > 1:
                self.lb.insert("end", f"=== 重复组（{len(file_list)}个文件）===")
                for f in file_list:
                    size = f.stat().st_size // 1024
                    self.lb.insert("end", f"  {f.relative_to(self.folder)} ({size} KB)")
                    self.duplicates[str(f)] = h
                dup_count += len(file_list) - 1
        
        self.status.config(text=f"✅ 找到 {dup_count} 个重复文件")
    
    def delete_selected(self):
        sel = self.lb.curselection()
        if not sel:
            messagebox.showwarning("提示", "请选择要删除的文件")
            return
        
        to_delete = []
        for idx in sel:
            text = self.lb.get(idx)
            if text.startswith("  "):
                path_str = text.strip().split(" ")[0]
                to_delete.append(Path(self.folder) / path_str)
        
        if not to_delete:
            messagebox.showwarning("提示", "请选择文件（不是分组标题）")
            return
        
        if messagebox.askyesno("确认删除", f"确定删除 {len(to_delete)} 个文件？"):
            ok = 0
            for f in to_delete:
                try:
                    f.unlink()
                    ok += 1
                except Exception as e:
                    print(f"删除失败: {e}")
            
            messagebox.showinfo("完成", f"已删除 {ok} 个文件")
            self.scan()

if __name__ == "__main__":
    import tkinter.ttk
    root = tk.Tk()
    App(root)
    root.mainloop()
