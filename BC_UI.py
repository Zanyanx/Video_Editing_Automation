import os
import math
import random
from tkinter import *
from tkinter import filedialog
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, TextClip, vfx
import moviepy.editor as mp
import moviepy.config as mp_config

# 设置FFmpeg路径
mp.ffmpeg_tools.ffmpeg_binary = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')

# 设置 ImageMagick 的路径
mp_config.IMAGEMAGICK_BINARY = os.path.join(os.getcwd(), 'imagemagick', 'magick.exe')
os.environ['MAGICK_HOME'] = os.path.join(os.getcwd(), 'imagemagick')
os.environ['PATH'] += os.pathsep + os.environ['MAGICK_HOME']

def get_random_image(folder_path):
    # 获取文件夹下所有文件的完整路径
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
    # 过滤出图像文件
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if not image_files:
        raise FileNotFoundError("No image files found in the specified folder.")

    # 从图像文件中随机选择一个
    random_image = random.choice(image_files)
    return random_image

def select_input_folder():
    folder = filedialog.askdirectory()
    input_path.set(folder)

def select_output_folder():
    folder = filedialog.askdirectory()
    output_path.set(folder)

def select_audio_file():
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    audio_path.set(file)

def select_image_folder():
    folder = filedialog.askdirectory()
    image_path.set(folder)

def start_processing():
    input_dir = input_path.get()
    audio_file = audio_path.get()
    output_dir = output_path.get()
    image_dir = image_path.get()
    clip_time = float(entry_clip_time.get())
    repeat_rate = float(entry_repeat_rate.get())
    acceleration_factor = float(entry_acceleration_factor.get())
    size_w = int(entry_size_w.get())
    size_h = int(entry_size_h.get())
    angle = int(entry_angle.get())
    text = entry_text.get()

    audio = AudioFileClip(audio_file)
    files = os.listdir(input_dir)
    for file in files:
        if file.endswith('MP4') or file.endswith('mp4'):
            file_path = os.path.join(input_dir, file)
            original_clip = VideoFileClip(file_path).rotate(angle).resize((size_w, size_h))

            # 加速视频
            faster_clip = original_clip.speedx(factor=acceleration_factor)
            duration = faster_clip.duration
            count = 0
            flag = 0
            for i in range(math.ceil(duration / clip_time)):
                if i == 0:
                    start_time = 0
                    end_time = clip_time
                else:
                    start_time = end_time - clip_time * repeat_rate
                    end_time = start_time + clip_time
                if start_time > duration:
                    break
                elif start_time < 0:
                    start_time = end_time
                if end_time >= duration:
                    end_time = duration
                sub_clip = faster_clip.subclip(start_time, end_time)
                if flag == 0:
                    sub_clip = sub_clip.fx(vfx.mirror_x)
                    flag = 1
                elif flag == 1:
                    flag = 2
                else:
                    image_path1 = get_random_image(image_dir)
                    image_clip1 = ImageClip(image_path1).set_duration(sub_clip.duration)
                    image_clip1 = image_clip1.set_pos(("right", "top")).resize(height=300)
                    image_path2 = get_random_image(image_dir)
                    image_clip2 = ImageClip(image_path2).set_duration(sub_clip.duration)
                    image_clip2 = image_clip2.set_pos(("right", "bottom")).resize(height=300)
                    image_path3 = get_random_image(image_dir)
                    image_clip3 = ImageClip(image_path3).set_duration(sub_clip.duration)
                    image_clip3 = image_clip3.set_pos(("left", "bottom")).resize(height=300)
                    sub_clip = CompositeVideoClip([sub_clip, image_clip1, image_clip2, image_clip3])
                    flag = 0
                count += 1
                txt_clip = TextClip(text, fontsize=120, font='./font/new.ttf', method='caption', color='black', size=(sub_clip.w, None))
                txt_clip = txt_clip.set_position(('center', sub_clip.h - 93 - txt_clip.h)).set_duration(sub_clip.duration)
                shadow_text = TextClip(text, fontsize=120, font='./font/new.ttf', method='caption', color='white', size=(sub_clip.w, None))
                shadow_text = shadow_text.set_position(('center', sub_clip.h - 100 - txt_clip.h)).set_duration(sub_clip.duration)
                clip = CompositeVideoClip([sub_clip, txt_clip]).without_audio()
                clip = CompositeVideoClip([clip, shadow_text]).set_audio(audio)
                output_file = f"{output_dir}/{file.split('.')[0]}_{count}.mp4"
                clip.write_videofile(output_file)

# 创建主窗口
root = Tk()
root.title("视频处理工具")

input_path = StringVar()
audio_path = StringVar()
output_path = StringVar()
image_path = StringVar()

# 输入文件夹
Label(root, text="选择输入文件夹:").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=input_path, width=50).grid(row=0, column=1, padx=10, pady=5)
Button(root, text="浏览", command=select_input_folder).grid(row=0, column=2, padx=10, pady=5)

# 音频文件
Label(root, text="选择音频文件:").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=audio_path, width=50).grid(row=1, column=1, padx=10, pady=5)
Button(root, text="浏览", command=select_audio_file).grid(row=1, column=2, padx=10, pady=5)

# 免扣贴纸文件夹
Label(root, text="选择免扣贴纸文件夹:").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=image_path, width=50).grid(row=2, column=1, padx=10, pady=5)
Button(root, text="浏览", command=select_image_folder).grid(row=2, column=2, padx=10, pady=5)

# 输出文件夹
Label(root, text="选择输出文件夹:").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=output_path, width=50).grid(row=3, column=1, padx=10, pady=5)
Button(root, text="浏览", command=select_output_folder).grid(row=3, column=2, padx=10, pady=5)

# 输入框
Label(root, text="片段持续时间:").grid(row=4, column=0, padx=10, pady=5)
entry_clip_time = Entry(root)
entry_clip_time.grid(row=4, column=1, padx=10, pady=5)

Label(root, text="重复率 (0.3 表示 30%):").grid(row=5, column=0, padx=10, pady=5)
entry_repeat_rate = Entry(root)
entry_repeat_rate.grid(row=5, column=1, padx=10, pady=5)

Label(root, text="播放倍速 (>1 加速, <1 减速):").grid(row=6, column=0, padx=10, pady=5)
entry_acceleration_factor = Entry(root)
entry_acceleration_factor.grid(row=6, column=1, padx=10, pady=5)

Label(root, text="视频宽度:").grid(row=7, column=0, padx=10, pady=5)
entry_size_w = Entry(root)
entry_size_w.grid(row=7, column=1, padx=10, pady=5)

Label(root, text="视频高度:").grid(row=8, column=0, padx=10, pady=5)
entry_size_h = Entry(root)
entry_size_h.grid(row=8, column=1, padx=10, pady=5)

Label(root, text="逆时针旋转度数:").grid(row=9, column=0, padx=10, pady=5)
entry_angle = Entry(root)
entry_angle.grid(row=9, column=1, padx=10, pady=5)

Label(root, text="需要显示的文案:").grid(row=10, column=0, padx=10, pady=5)
entry_text = Entry(root)
entry_text.grid(row=10, column=1, padx=10, pady=5)

# 开始按钮
Button(root, text="开始处理", command=start_processing).grid(row=11, column=1, padx=10, pady=20)

root.mainloop()
