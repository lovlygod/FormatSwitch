import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from pathlib import Path
import threading

try:
    from format_converter import csv_to_json, json_to_csv, excel_to_json, excel_to_csv, json_to_excel, csv_to_excel
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from format_converter import csv_to_json, json_to_csv, excel_to_json, excel_to_csv, json_to_excel, csv_to_excel


class DarkThemeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("FormatSwitch - Конвертер файлов")
        self.root.geometry("700x500")
        
        self.setup_dark_theme()
        
        self.create_widgets()
        
    def setup_dark_theme(self):
        self.root.configure(bg='#2e2e2e')
        
        self.colors = {
            'bg': '#2e2e2e',
            'fg': '#ffffff',
            'button_bg': '#4a4a4a',
            'button_fg': '#ffffff',
            'entry_bg': '#3c3c3c',
            'entry_fg': '#ffffff',
            'frame_bg': '#2e2e2e',
            'label_fg': '#ffffff',
            'combo_bg': '#3c3c3c',
            'combo_fg': '#ffffff',
            'combo_field_bg': '#3c3c',
            'progress_bg': '#3c3c3c',
            'progress_fg': '#4CAF50'
        }
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TFrame', background=self.colors['frame_bg'])
        self.style.configure('TLabel', background=self.colors['frame_bg'], foreground=self.colors['label_fg'])
        self.style.configure('TButton', background=self.colors['button_bg'], foreground=self.colors['button_fg'])
        self.style.configure('TEntry', fieldbackground=self.colors['entry_bg'], foreground=self.colors['entry_fg'])
        self.style.configure('TCombobox', fieldbackground=self.colors['combo_field_bg'], 
                            background=self.colors['combo_bg'], foreground=self.colors['combo_fg'])
        self.style.map('TButton', background=[('active', '#5a5a5a')])
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="FormatSwitch", font=("Arial", 20, "bold"), 
                              bg=self.colors['bg'], fg=self.colors['fg'])
        title_label.pack(pady=(0, 20))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Входной файл:", font=("Arial", 10)).pack(anchor=tk.W)
        
        input_file_frame = ttk.Frame(input_frame)
        input_file_frame.pack(fill=tk.X, pady=5)
        
        self.input_file_var = tk.StringVar()
        self.input_entry = tk.Entry(input_file_frame, textvariable=self.input_file_var, 
                                   bg=self.colors['entry_bg'], fg=self.colors['entry_fg'], 
                                   insertbackground=self.colors['entry_fg'], relief=tk.FLAT)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 10))
        
        ttk.Button(input_file_frame, text="Выбрать", command=self.select_input_file).pack(side=tk.RIGHT)
        
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Выходной файл:", font=("Arial", 10)).pack(anchor=tk.W)
        
        output_file_frame = ttk.Frame(output_frame)
        output_file_frame.pack(fill=tk.X, pady=5)
        
        self.output_file_var = tk.StringVar()
        self.output_entry = tk.Entry(output_file_frame, textvariable=self.output_file_var, 
                                    bg=self.colors['entry_bg'], fg=self.colors['entry_fg'], 
                                    insertbackground=self.colors['entry_fg'], relief=tk.FLAT)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 10))
        
        ttk.Button(output_file_frame, text="Выбрать", command=self.select_output_file).pack(side=tk.RIGHT)
        
        conversion_frame = ttk.Frame(main_frame)
        conversion_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(conversion_frame, text="Тип конвертации:", font=("Arial", 10)).pack(anchor=tk.W)
        
        self.conversion_type = tk.StringVar()
        conversion_types = [
            ("CSV → JSON", "csv_to_json"),
            ("JSON → CSV", "json_to_csv"),
            ("Excel → JSON", "excel_to_json"),
            ("Excel → CSV", "excel_to_csv"),
            ("JSON → Excel", "json_to_excel"),
            ("CSV → Excel", "csv_to_excel")
        ]
        
        conversion_type_frame = ttk.Frame(conversion_frame)
        conversion_type_frame.pack(fill=tk.X, pady=5)
        
        for text, value in conversion_types:
            ttk.Radiobutton(conversion_type_frame, text=text, variable=self.conversion_type, 
                           value=value).pack(anchor=tk.W, side=tk.LEFT, padx=(0, 15))
        
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(options_frame, text="Дополнительные опции:", font=("Arial", 10)).pack(anchor=tk.W)
        
        options_inner_frame = ttk.Frame(options_frame)
        options_inner_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(options_inner_frame, text="Имя листа Excel (если применимо):").pack(anchor=tk.W)
        self.sheet_name_var = tk.StringVar()
        self.sheet_entry = tk.Entry(options_inner_frame, textvariable=self.sheet_name_var, 
                                   bg=self.colors['entry_bg'], fg=self.colors['entry_fg'], 
                                   insertbackground=self.colors['entry_fg'], relief=tk.FLAT)
        self.sheet_entry.pack(fill=tk.X, pady=5)
        
        self.convert_button = ttk.Button(main_frame, text="Конвертировать", 
                                        command=self.start_conversion)
        self.convert_button.pack(pady=20)
        
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к конвертации")
        status_label = tk.Label(main_frame, textvariable=self.status_var, 
                               bg=self.colors['bg'], fg=self.colors['fg'])
        status_label.pack(pady=5)
    
    def select_input_file(self):
        filetypes = [
            ("Все поддерживаемые форматы", "*.csv *.json *.xlsx *.xls"),
            ("CSV файлы", "*.csv"),
            ("JSON файлы", "*.json"),
            ("Excel файлы", "*.xlsx *.xls"),
            ("Все файлы", "*.*")
        ]
        filename = filedialog.askopenfilename(title="Выберите входной файл", filetypes=filetypes)
        if filename:
            self.input_file_var.set(filename)
            self.auto_fill_output_path(filename)
    
    def select_output_file(self):
        if self.conversion_type.get():
            ext_map = {
                'csv_to_json': '.json',
                'json_to_csv': '.csv',
                'excel_to_json': '.json',
                'excel_to_csv': '.csv',
                'json_to_excel': '.xlsx',
                'csv_to_excel': '.xlsx'
            }
            default_ext = ext_map.get(self.conversion_type.get(), '')
            filetypes = [(f"{default_ext.upper()[1:]} файлы", f"*{default_ext}")]
            
            filename = filedialog.asksaveasfilename(title="Сохранить результат", 
                                                  defaultextension=default_ext, filetypes=filetypes)
            if filename:
                self.output_file_var.set(filename)
        else:
            messagebox.showwarning("Предупреждение", "Сначала выберите тип конвертации")
    
    def auto_fill_output_path(self, input_path):
        if not self.conversion_type.get():
            return
            
        input_path = Path(input_path)
        ext_map = {
            'csv_to_json': '.json',
            'json_to_csv': '.csv',
            'excel_to_json': '.json',
            'excel_to_csv': '.csv',
            'json_to_excel': '.xlsx',
            'csv_to_excel': '.xlsx'
        }
        
        default_ext = ext_map.get(self.conversion_type.get())
        if default_ext:
            output_path = input_path.with_suffix(default_ext)
            self.output_file_var.set(str(output_path))
    
    def start_conversion(self):
        if not self.validate_inputs():
            return
            
        thread = threading.Thread(target=self.perform_conversion)
        thread.daemon = True
        thread.start()
    
    def validate_inputs(self):
        if not self.input_file_var.get():
            messagebox.showerror("Ошибка", "Выберите входной файл")
            return False
        
        if not self.output_file_var.get():
            messagebox.showerror("Ошибка", "Выберите выходной файл")
            return False
        
        if not self.conversion_type.get():
            messagebox.showerror("Ошибка", "Выберите тип конвертации")
            return False
        
        if not os.path.exists(self.input_file_var.get()):
            messagebox.showerror("Ошибка", "Входной файл не существует")
            return False
        
        return True
    
    def perform_conversion(self):
        try:
            self.root.after(0, lambda: self.convert_button.configure(state='disabled'))
            self.root.after(0, lambda: self.status_var.set("Конвертация в процессе..."))
            self.root.after(0, lambda: self.progress.configure(value=0))
            
            input_path = self.input_file_var.get()
            output_path = self.output_file_var.get()
            conversion_type = self.conversion_type.get()
            sheet_name = self.sheet_name_var.get() if self.sheet_name_var.get() else None
            
            if conversion_type == 'csv_to_json':
                csv_to_json(input_path, output_path)
            elif conversion_type == 'json_to_csv':
                json_to_csv(input_path, output_path)
            elif conversion_type == 'excel_to_json':
                excel_to_json(input_path, output_path, sheet_name)
            elif conversion_type == 'excel_to_csv':
                excel_to_csv(input_path, output_path, sheet_name)
            elif conversion_type == 'json_to_excel':
                json_to_excel(input_path, output_path)
            elif conversion_type == 'csv_to_excel':
                csv_to_excel(input_path, output_path)
            
            self.root.after(0, lambda: self.progress.configure(value=100))
            self.root.after(0, lambda: self.status_var.set("Конвертация завершена успешно!"))
            self.root.after(0, lambda: messagebox.showinfo("Успех", f"Файл успешно конвертирован:\n{output_path}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Ошибка: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Произошла ошибка при конвертации:\n{str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.convert_button.configure(state='enabled'))
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = DarkThemeConverter(root)
    app.run()