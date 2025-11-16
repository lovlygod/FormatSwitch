import argparse
import csv
import json
import pandas as pd
import sys
from pathlib import Path


def csv_to_json(csv_file_path, json_file_path):
    """
    Конвертирует CSV файл в JSON
    """
    try:
        data = []
        encodings = ['utf-8', 'utf-8-sig', 'cp1251', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        data.append(row)
                break
            except UnicodeDecodeError:
                if encoding == encodings[-1]:
                    raise
                continue
        
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
        
        print(f"Файл {csv_file_path} успешно конвертирован в {json_file_path}")
    except Exception as e:
        print(f"Ошибка при конвертации CSV в JSON: {str(e)}")
        raise


def json_to_csv(json_file_path, csv_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        if not data:
            print("JSON файл пуст или содержит недопустимые данные")
            return
        
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            if isinstance(data[0], dict):
                fieldnames = data[0].keys()
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerows(data)
            else:
                fieldnames = range(len(data[0]))
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(fieldnames)
                csv_writer.writerows(data)
        
        print(f"Файл {json_file_path} успешно конвертирован в {csv_file_path}")
    except Exception as e:
        print(f"Ошибка при конвертации JSON в CSV: {str(e)}")
        raise


def excel_to_json(excel_file_path, json_file_path, sheet_name=None):
    try:
        if sheet_name is None:
            df = pd.read_excel(excel_file_path, sheet_name=0)
        else:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        
        if isinstance(df, dict):
            if sheet_name is None:
                df = df[list(df.keys())[0]]
            else:
                df = df[sheet_name]
        
        data = df.to_dict(orient='records')
        
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
        
        print(f"Файл {excel_file_path} успешно конвертирован в {json_file_path}")
    except ValueError as e:
        if "sheet" in str(e).lower():
            available_sheets = pd.ExcelFile(excel_file_path).sheet_names
            print(f"Ошибка: Лист '{sheet_name}' не найден. Доступные листы: {available_sheets}")
        else:
            raise e


def excel_to_csv(excel_file_path, csv_file_path, sheet_name=None):
    """
    Конвертирует Excel файл в CSV
    """
    try:
        if sheet_name is None:
            df = pd.read_excel(excel_file_path, sheet_name=0)
        else:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        
        if isinstance(df, dict):
            if sheet_name is None:
                df = df[list(df.keys())[0]]
            else:
                df = df[sheet_name]
        
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        
        print(f"Файл {excel_file_path} успешно конвертирован в {csv_file_path}")
    except ValueError as e:
        if "sheet" in str(e).lower():
            available_sheets = pd.ExcelFile(excel_file_path).sheet_names
            print(f"Ошибка: Лист '{sheet_name}' не найден. Доступные листы: {available_sheets}")
        else:
            raise e


def json_to_excel(json_file_path, excel_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        df = pd.DataFrame(data)
        df.to_excel(excel_file_path, index=False)
        
        print(f"Файл {json_file_path} успешно конвертирован в {excel_file_path}")
    except Exception as e:
        print(f"Ошибка при конвертации JSON в Excel: {str(e)}")
        raise


def csv_to_excel(csv_file_path, excel_file_path):
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        df.to_excel(excel_file_path, index=False)
        
        print(f"Файл {csv_file_path} успешно конвертирован в {excel_file_path}")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, encoding='cp1251')
        df.to_excel(excel_file_path, index=False)
        
        print(f"Файл {csv_file_path} успешно конвертирован в {excel_file_path} (использована кодировка cp1251)")
    except Exception as e:
        print(f"Ошибка при конвертации CSV в Excel: {str(e)}")
        raise


def main():
    parser = argparse.ArgumentParser(description='Утилита для конвертации между форматами CSV, JSON и Excel')
    parser.add_argument('input_file', help='Входной файл')
    parser.add_argument('output_file', help='Выходной файл')
    parser.add_argument('--sheet', help='Имя листа Excel (для конвертации из Excel)')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)
    
    input_ext = input_path.suffix.lower()
    output_ext = output_path.suffix.lower()
    
    if not input_path.exists():
        print(f"Ошибка: Входной файл {input_path} не существует")
        sys.exit(1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if input_ext == '.csv' and output_ext == '.json':
            csv_to_json(input_path, output_path)
        elif input_ext == '.json' and output_ext == '.csv':
            json_to_csv(input_path, output_path)
        elif input_ext == '.xlsx' and output_ext == '.json':
            excel_to_json(input_path, output_path, args.sheet)
        elif input_ext == '.xls' and output_ext == '.json':
            excel_to_json(input_path, output_path, args.sheet)
        elif input_ext == '.xlsx' and output_ext == '.csv':
            excel_to_csv(input_path, output_path, args.sheet)
        elif input_ext == '.xls' and output_ext == '.csv':
            excel_to_csv(input_path, output_path, args.sheet)
        elif input_ext == '.json' and output_ext == '.xlsx':
            json_to_excel(input_path, output_path)
        elif input_ext == '.csv' and output_ext == '.xlsx':
            csv_to_excel(input_path, output_path)
        else:
            print(f"Ошибка: Конвертация из {input_ext} в {output_ext} не поддерживается")
            print("Поддерживаемые форматы: CSV, JSON, XLSX, XLS")
            sys.exit(1)
    
    except Exception as e:
        print(f"Ошибка при конвертации: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()