import os
import glob
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox

def fb2_to_txt(fb2_file, output_folder):
    try:
        tree = ET.parse(fb2_file)
        root = tree.getroot()
        
        namespace = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
        body = root.find('fb2:body', namespace)
        
        if body is None:
            print(f"[Ошибка] Нет содержимого в: {fb2_file}")
            return
        
        text_content = []
        for paragraph in body.findall('.//fb2:p', namespace):
            text_content.append(paragraph.text if paragraph.text else '')
        
        txt_file = os.path.join(output_folder, os.path.basename(fb2_file).replace(".fb2", ".txt"))
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text_content))
        
        print(f"[Успешно] {fb2_file} -> {txt_file}")
    except Exception as e:
        print(f"[Ошибка] {fb2_file}: {e}")

def txt_to_fb2(txt_file, output_folder):
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            text_content = f.readlines()
        
        fb2_content = """<?xml version='1.0' encoding='utf-8'?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">
    <body>
        <section>
"""
        for line in text_content:
            fb2_content += f"            <p>{line.strip()}</p>\n"
        fb2_content += """
        </section>
    </body>
</FictionBook>
"""
        
        fb2_file = os.path.join(output_folder, os.path.basename(txt_file).replace(".txt", ".fb2"))
        with open(fb2_file, 'w', encoding='utf-8') as f:
            f.write(fb2_content)
        
        print(f"[Успешно] {txt_file} -> {fb2_file}")
    except Exception as e:
        print(f"[Ошибка] {txt_file}: {e}")

def select_fb2_files():
    files = filedialog.askopenfilenames(title="Выберите файлы .fb2", filetypes=[("FictionBook", "*.fb2")])
    return files

def select_txt_files():
    files = filedialog.askopenfilenames(title="Выберите файлы .txt", filetypes=[("Text Files", "*.txt")])
    return files

def select_output_folder():
    folder = filedialog.askdirectory(title="Выберите папку для сохранения файлов")
    return folder

def merge_txt_files():
    txt_files = select_txt_files()
    if not txt_files:
        messagebox.showwarning("Предупреждение", "Вы не выбрали файлы .txt")
        return
    
    output_folder = select_output_folder()
    if not output_folder:
        messagebox.showwarning("Предупреждение", "Вы не выбрали папку для сохранения объединенного .txt файла")
        return
    
    output_file = os.path.join(output_folder, "merged.txt")
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for txt_file in txt_files:
            with open(txt_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read() + '\n')
    
    messagebox.showinfo("Готово", "Файлы успешно объединены в merged.txt")

def convert_txt_to_fb2():
    txt_files = select_txt_files()
    if not txt_files:
        messagebox.showwarning("Предупреждение", "Вы не выбрали файлы .txt")
        return
    
    output_folder = select_output_folder()
    if not output_folder:
        messagebox.showwarning("Предупреждение", "Вы не выбрали папку для сохранения .fb2 файлов")
        return
    
    for txt_file in txt_files:
        txt_to_fb2(txt_file, output_folder)
    
    messagebox.showinfo("Готово", "Все файлы успешно конвертированы в .fb2!")

def start_conversion():
    fb2_files = select_fb2_files()
    if not fb2_files:
        messagebox.showwarning("Предупреждение", "Вы не выбрали файлы .fb2")
        return
    
    output_folder = select_output_folder()
    if not output_folder:
        messagebox.showwarning("Предупреждение", "Вы не выбрали папку для сохранения .txt файлов")
        return
    
    for fb2_file in fb2_files:
        fb2_to_txt(fb2_file, output_folder)
    
    messagebox.showinfo("Готово", "Все файлы успешно конвертированы!")

def main():
    root = tk.Tk()
    root.title("FB2 и TXT Конвертер")
    root.geometry("400x300")
    
    tk.Label(root, text="Выберите файлы и операцию").pack(pady=10)
    tk.Button(root, text="FB2 → TXT", command=start_conversion).pack(pady=10)
    tk.Button(root, text="TXT → FB2", command=convert_txt_to_fb2).pack(pady=10)
    tk.Button(root, text="Объединить .txt файлы", command=merge_txt_files).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
