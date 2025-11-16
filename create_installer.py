import os
import sys
import subprocess
import shutil
from pathlib import Path


def create_executable():
    """Создание исполняемого файла с помощью PyInstaller"""
    try:
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=FormatSwitch',
            '--add-data=README.md;.',
            '--hidden-import=pandas',
            '--hidden-import=openpyxl',
            '--hidden-import=xlrd',
            'gui_converter.py'
        ]
        
        print("Создание исполняемого файла...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Ошибка при создании исполняемого файла: {result.stderr}")
            return False
        
        print("Исполняемый файл успешно создан!")
        return True
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return False


def create_installer():
    inno_script = """
[Setup]
AppName=FormatSwitch
AppVersion=1.0.0
DefaultDirName={autopf}\\FormatSwitch
DefaultGroupName=FormatSwitch
StartMenuGroupName=FormatSwitch
UninstallDisplayIcon={app}\\FormatSwitch.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\\FormatSwitch.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\FormatSwitch"; Filename: "{app}\\FormatSwitch.exe"
Name: "{group}\\{cm:UninstallProgram,FormatSwitch}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\\FormatSwitch"; Filename: "{app}\\FormatSwitch.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительные задачи:"

[Run]
Filename: "{app}\\FormatSwitch.exe"; Description: "Запустить FormatSwitch"; Flags: nowait postinstall skipifsilent
"""
    
    with open('format_switch_installer.iss', 'w', encoding='utf-8') as f:
        f.write(inno_script)
    
    print("Создан скрипт установщика Inno Setup: format_switch_installer.iss")
    print("Для создания установщика выполните: iscc format_switch_installer.iss")
    print("(Требуется установленный Inno Setup Compiler)")


def create_portable_version():
    """Создание портативной версии приложения"""
    try:
        if os.path.exists('portable'):
            shutil.rmtree('portable')
        
        if not create_executable():
            return False
        
        os.makedirs('portable', exist_ok=True)
        
        shutil.copytree('dist', 'portable/dist', dirs_exist_ok=True)
        
        os.makedirs('portable/examples', exist_ok=True)
        
        for example_file in ['test_data.csv', 'test_data_from_excel.json', 'test_data.xlsx']:
            if os.path.exists(example_file):
                shutil.copy(example_file, f'portable/examples/{example_file}')
        
        if os.path.exists('README.md'):
            shutil.copy('README.md', 'portable/')
        
        print("Портативная версия создана в папке 'portable'")
        return True
        
    except Exception as e:
        print(f"Произошла ошибка при создании портативной версии: {str(e)}")
        return False


def main():
    print("Создание установщика для FormatSwitch...")
    
    if not create_executable():
        print("Не удалось создать исполняемый файл")
        sys.exit(1)
    
    create_installer()
    
    if create_portable_version():
        print("Портативная версия создана успешно")
    
    print("\nУстановка завершена!")
    print("1. Исполняемый файл находится в папке 'dist'")
    print("2. Скрипт установщика Inno Setup создан как 'format_switch_installer.iss'")
    print("3. Портативная версия доступна в папке 'portable'")


if __name__ == "__main__":
    main()