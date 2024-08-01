import os
import random
import itertools
from tkinter import *
from tkinter import filedialog
from moviepy.editor import VideoFileClip, CompositeVideoClip
import moviepy.editor as mp
import moviepy.config as mp_config

# 设置FFmpeg路径
mp.ffmpeg_tools.ffmpeg_binary = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')

# 设置 ImageMagick 的路径
mp_config.IMAGEMAGICK_BINARY = os.path.join(os.getcwd(), 'imagemagick', 'magick.exe')
os.environ['MAGICK_HOME'] = os.path.join(os.getcwd(), 'imagemagick')
os.environ['PATH'] += os.pathsep + os.environ['MAGICK_HOME']

def list_files_in_directory(directory):
    try:
        # 获取目录中的所有文件和文件夹
        files_and_dirs = os.listdir(directory)

        # 过滤出文件名（包含后缀）
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory, f))]
        return files
    except Exception as e:
        print(f"Error: {e}")
        return []

def montage_1(clip1, clip2, clip3, clip4):
    final_clip = CompositeVideoClip([clip1, clip2.set_start(clip1.duration).crossfadein(0.25), clip3.set_start(clip1.duration+clip2.duration).crossfadein(0.25), clip4.set_start(clip1.duration+clip2.duration+clip3.duration).crossfadeout(0.25)])
    return final_clip

def select_folder(var):
    folder = filedialog.askdirectory()
    var.set(folder)

def select_output_folder():
    folder = filedialog.askdirectory()
    output_path.set(folder)

def start_processing():
    folder1 = folder_path1.get()
    folder2 = folder_path2.get()
    folder3 = folder_path3.get()
    folder4 = folder_path4.get()
    output_dir = output_path.get()
    num = int(num_videos.get())

    clips_folder1 = list_files_in_directory(folder1)
    clips_folder2 = list_files_in_directory(folder2)
    clips_folder3 = list_files_in_directory(folder3)
    clips_folder4 = list_files_in_directory(folder4)

    combinations = list(itertools.product(clips_folder1, clips_folder2, clips_folder3, clips_folder4))
    selected_combinations = random.sample(combinations, min(num, len(combinations)))

    for i, combination in enumerate(selected_combinations):
        path1 = os.path.join(folder1, combination[0])
        path2 = os.path.join(folder2, combination[1])
        path3 = os.path.join(folder3, combination[2])
        path4 = os.path.join(folder4, combination[3])
        clip1 = VideoFileClip(path1)
        clip2 = VideoFileClip(path2)
        clip3 = VideoFileClip(path3)
        clip4 = VideoFileClip(path4)
        video = montage_1(clip1, clip2, clip3, clip4)
        output = os.path.join(output_dir, f"{i+1}.mp4")
        video.write_videofile(output)

# 创建主窗口
root = Tk()
root.title("视频组合工具")

folder_path1 = StringVar()
folder_path2 = StringVar()
folder_path3 = StringVar()
folder_path4 = StringVar()
output_path = StringVar()
num_videos = StringVar()

# 输入文件夹
Label(root, text="选择第一个片段的文件夹:").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=folder_path1, width=50).grid(row=0, column=1, padx=10, pady=5)
Button(root, text="浏览", command=lambda: select_folder(folder_path1)).grid(row=0, column=2, padx=10, pady=5)

Label(root, text="选择第二个片段的文件夹:").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=folder_path2, width=50).grid(row=1, column=1, padx=10, pady=5)
Button(root, text="浏览", command=lambda: select_folder(folder_path2)).grid(row=1, column=2, padx=10, pady=5)

Label(root, text="选择第三个片段的文件夹:").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=folder_path3, width=50).grid(row=2, column=1, padx=10, pady=5)
Button(root, text="浏览", command=lambda: select_folder(folder_path3)).grid(row=2, column=2, padx=10, pady=5)

Label(root, text="选择第四个片段的文件夹:").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=folder_path4, width=50).grid(row=3, column=1, padx=10, pady=5)
Button(root, text="浏览", command=lambda: select_folder(folder_path4)).grid(row=3, column=2, padx=10, pady=5)

# 输出文件夹
Label(root, text="选择输出文件夹:").grid(row=4, column=0, padx=10, pady=5)
Entry(root, textvariable=output_path, width=50).grid(row=4, column=1, padx=10, pady=5)
Button(root, text="浏览", command=select_output_folder).grid(row=4, column=2, padx=10, pady=5)

# 输入框
Label(root, text="希望得到的视频条数:").grid(row=5, column=0, padx=10, pady=5)
Entry(root, textvariable=num_videos).grid(row=5, column=1, padx=10, pady=5)

# 开始按钮
Button(root, text="开始处理", command=start_processing).grid(row=6, column=1, padx=10, pady=20)

root.mainloop()
