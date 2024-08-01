from cx_Freeze import setup, Executable

# 添加必要的包和文件
build_exe_options = {
    "packages": ["os", "moviepy","moviepy.editor", "imageio", "imageio_ffmpeg","tkinter"],
    "include_files": [
        "font/",  # 添加 font 文件夹
        "ffmpeg/",
        "imagemagick/"
    ]
}

setup(
    name="Editingapp",
    version="1.0",
    description="Description of your program",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("BC.py", base=None, icon="./icon/1.ico"),
        Executable("Mix.py", base=None, icon="./icon/1.ico"),
        Executable("Mix_UI.py", base=None, icon="./icon/1.ico"),
        Executable("BC_UI.py", base=None, icon="./icon/1.ico")
    ]
)
