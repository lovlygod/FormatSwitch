import os
import sys
import subprocess
import shutil
from pathlib import Path


def create_app_directory():
    if os.path.exists('format_switch_app'):
        shutil.rmtree('format_switch_app')
    
    os.makedirs('format_switch_app/usr/bin', exist_ok=True)
    os.makedirs('format_switch_app/usr/share/applications', exist_ok=True)
    os.makedirs('format_switch_app/usr/share/icons/hicolor/256x256/apps', exist_ok=True)
    os.makedirs('format_switch_app/usr/share/doc/format-switch', exist_ok=True)
    
    shutil.copy('format_converter.py', 'format_switch_app/usr/bin/')
    shutil.copy('gui_converter.py', 'format_switch_app/usr/bin/')
    shutil.copy('README.md', 'format_switch_app/usr/share/doc/format-switch/')
    
    cli_script = """#!/bin/bash
python3 /usr/bin/format_converter.py "$@"
"""
    
    with open('format_switch_app/usr/bin/format-switch-cli', 'w') as f:
        f.write(cli_script)
    
    os.chmod('format_switch_app/usr/bin/format-switch-cli', 0o755)
    
    gui_script = """#!/bin/bash
python3 /usr/bin/gui_converter.py "$@"
"""
    
    with open('format_switch_app/usr/bin/format-switch', 'w') as f:
        f.write(gui_script)
    
    os.chmod('format_switch_app/usr/bin/format-switch', 0o75)
    
    desktop_file = """[Desktop Entry]
Version=1.0
Type=Application
Name=FormatSwitch
Comment=Утилита для конвертации между форматами CSV, JSON и Excel
Exec=/usr/bin/format-switch
Icon=format-switch
Terminal=false
Categories=Office;Utility;
"""
    
    with open('format_switch_app/usr/share/applications/format-switch.desktop', 'w') as f:
        f.write(desktop_file)
    
    with open('format_switch_app/usr/share/icons/hicolor/256x256/apps/format-switch.png', 'w') as f:
        f.write('')
    print("Структура пакета для Linux создана в папке 'format_switch_app'")


def create_deb_package():
    """Создание DEB пакета для Ubuntu/Debian"""
    if not os.path.exists('format_switch_app'):
        print("Сначала создайте директорию с приложением")
        return False
    
    os.makedirs('format_switch_app/DEBIAN', exist_ok=True)
    
    control_file = """Package: format-switch
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pandas, python3-openpyxl
Maintainer: FormatSwitch Team
Description: Утилита для конвертации между форматами CSV, JSON и Excel
 FormatSwitch - это инструмент для конвертации файлов между различными
 форматами данных: CSV, JSON, XLSX, XLS. Включает в себя как консольный,
 так и графический интерфейс.
"""
    
    with open('format_switch_app/DEBIAN/control', 'w') as f:
        f.write(control_file)
    
    postinst_script = """#!/bin/bash
# Устанавливаем зависимости, если они не установлены
if ! python3 -c "import pandas" 2>/dev/null; then
    pip3 install pandas openpyxl
fi
"""
    
    with open('format_switch_app/DEBIAN/postinst', 'w') as f:
        f.write(postinst_script)
    
    os.chmod('format_switch_app/DEBIAN/postinst', 0o755)
    
    try:
        subprocess.run(['dpkg', '-b', 'format_switch_app', 'format-switch_1.0.0_all.deb'], 
                      check=True, capture_output=True)
        print("DEB пакет создан: format-switch_1.0.0_all.deb")
        return True
    except subprocess.CalledProcessError:
        print("Не удалось создать DEB пакет (возможно, dpkg не установлен)")
        return False


def create_rpm_package():
    """Создание RPM пакета для Fedora/CentOS"""
    if not os.path.exists('format_switch_app'):
        print("Сначала создайте директорию с приложением")
        return False
    
    spec_content = """Name:           format-switch
Version:        1.0
Release:        1%{?dist}
Summary:        Утилита для конвертации между форматами CSV, JSON и Excel

License:        GPL
BuildArch:      noarch

Requires:       python3, python3-pandas, python3-openpyxl

%description
FormatSwitch - это инструмент для конвертации файлов между различными
форматами данных: CSV, JSON, XLSX, XLS. Включает в себя как консольный,
так и графический интерфейс.

%files
/usr/bin/format_converter.py
/usr/bin/gui_converter.py
/usr/bin/format-switch-cli
/usr/bin/format-switch
/usr/share/applications/format-switch.desktop
/usr/share/icons/hicolor/256x256/apps/format-switch.png
/usr/share/doc/format-switch/README.md

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps
mkdir -p %{buildroot}/usr/share/doc/format-switch

cp format_converter.py %{buildroot}/usr/bin/
cp gui_converter.py %{buildroot}/usr/bin/
cp format-switch-cli %{buildroot}/usr/bin/format-switch-cli
cp format-switch %{buildroot}/usr/bin/format-switch
cp format-switch.desktop %{buildroot}/usr/share/applications/
cp format-switch.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/
cp README.md %{buildroot}/usr/share/doc/format-switch/

%post
# Устанавливаем зависимости, если они не установлены
if ! python3 -c "import pandas" 2>/dev/null; then
    pip3 install pandas openpyxl
fi

%changelog
* Sat Nov 16 2024 FormatSwitch Team - 1.0.0-1
- Initial package
"""
    
    with open('format-switch.spec', 'w') as f:
        f.write(spec_content)
    
    print("SPEC файл для RPM пакета создан: format-switch.spec")
    print("Для создания RPM пакета выполните: rpmbuild -bb format-switch.spec")
    print("(Требуется установленный rpm-build)")
    
    return True


def create_pip_package():
    setup_content = """from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="format-switch",
    version="1.0.0",
    author="FormatSwitch Team",
    author_email="formatswitch@example.com",
    description="Утилита для конвертации между форматами CSV, JSON и Excel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/format-switch",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
    ],
    entry_points={
        'console_scripts': [
            'format-switch-cli=format_converter:main',
            'format-switch-gui=gui_converter:main',
        ],
    },
)
"""
    
    with open('setup.py', 'w') as f:
        f.write(setup_content)
    
    pyproject_content = """[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "format-switch"
version = "1.0.0"
description = "Утилита для конвертации между форматами CSV, JSON и Excel"
readme = "README.md"
authors = [{name = "FormatSwitch Team", email = "formatswitch@example.com"}]
license = {text = "MIT"}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
requires-python = ">=3.6"
dependencies = [
    "pandas>=1.3.0",
    "openpyxl>=3.0.0",
]

[project.scripts]
format-switch-cli = "format_converter:main"
format-switch-gui = "gui_converter:main"
"""
    
    with open('pyproject.toml', 'w') as f:
        f.write(pyproject_content)
    
    print("Файлы для pip пакета созданы: setup.py и pyproject.toml")
    print("Для создания pip пакета выполните: python -m build")


def main():
    print("Создание пакета для Linux...")
    
    create_app_directory()
    
    create_deb_package()
    
    create_rpm_package()
    
    create_pip_package()
    
    print("\nПакеты для Linux созданы!")
    print("1. DEB пакет для Ubuntu/Debian")
    print("2. RPM spec файл для Fedora/CentOS")
    print("3. Файлы для pip пакета")


if __name__ == "__main__":
    main()