import os
import shutil

from copystatic import copy_files_recursive
from markdown_blocks import generate_page



dir_path_static = "./static"
dir_path_public = "./public"

dest_path ="./public/index.html"


def main():
    print(os.getcwd()) # gibt das working directory ausgehend von dem Ort an, an dem main.py gestartet wurde! Dies ist main.sh! Deswegen ist dir_path_static = "./static"  und nicht dir_path_static = "../static"  !!! Alternativ kann das workoing directory auch innerhalb einer Datei geändert werden, zB so:    os.chdir(os.path.dirname(os.path.abspath(__file__)))    __file__ gibt den absolut-Pfad für die gerade betrachtete Datei an, also die Datei, in der versucht wird das workingi directory zu ändern
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page("./content/index.md", "./template.html", dest_path)




main()