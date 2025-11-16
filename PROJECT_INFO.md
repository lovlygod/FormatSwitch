# FormatSwitch - Информация о проекте

## Описание
FormatSwitch - это инструмент для конвертации файлов между различными форматами данных: CSV, JSON, XLSX, XLS. Включает в себя как консольный, так и графический интерфейс.

## Структура проекта

```
FormatSwitch/
├── format_converter.py     # Основной модуль конвертации форматов
├── gui_converter.py        # Графический интерфейс
├── create_installer.py     # Создание установщика для Windows
├── create_linux_package.py # Создание пакета для Linux
├── requirements.txt        # Зависимости
├── README.md               # Документация (EN)
├── README-RU.md            # Документация (RU)
├── LICENSE                 # Лицензия проекта
├── .gitignore              # Файлы, игнорируемые Git
└── PROJECT_INFO.md         # Информация о проекте
```

## Функциональность

### CLI (Консольный интерфейс)
- Конвертация CSV → JSON
- Конвертация JSON → CSV
- Конвертация Excel → JSON
- Конвертация Excel → CSV
- Конвертация JSON → Excel
- Конвертация CSV → Excel

### GUI (Графический интерфейс)
- Темная тема интерфейса
- Поддержка всех форматов
- Удобное управление файлами
- Прогресс-бар конвертации

## Зависимости
- pandas>=1.3.0
- openpyxl>=3.0.0
- pyinstaller>=5.0.0

## Установка и запуск

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск CLI
```bash
python format_converter.py input.csv output.json
```

### Запуск GUI
```bash
python gui_converter.py
```

## Поддерживаемые форматы
- CSV (Comma-Separated Values)
- JSON (JavaScript Object Notation)
- XLSX (Excel Open XML)
- XLS (Excel Legacy Format)