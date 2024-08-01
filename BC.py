import os
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, TextClip, vfx
import math
import random
import moviepy.editor as mp
import moviepy.config as mp_config

# 设置FFmpeg路径
mp.ffmpeg_tools.ffmpeg_binary = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')

# 设置 ImageMagick 的路径
mp_config.IMAGEMAGICK_BINARY = os.path.join(os.getcwd(), 'imagemagick', 'magick.exe')
os.environ['MAGICK_HOME'] = os.path.join(os.getcwd(), 'imagemagick')
os.environ['PATH'] += os.pathsep + os.environ['MAGICK_HOME']

# print("FFmpeg路径:", mp.ffmpeg_tools.ffmpeg_binary)
# print("ImageMagick路径:", os.environ['MAGICK_HOME'])

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

print('请按照提示的文字输入内容，回车表示输入完成')
###素材库所在的文件夹位置###
path = input('请输入待裁剪的素材文件夹位置：')
###口播配音的路径###
audio_path = input('请输入配音文件的完整路径：')
audio = AudioFileClip(audio_path)
image_clip_path = input('请输入免扣贴纸的文件夹路径：')
###保存的文件夹位置###
output_path = input('请输入保存文件夹位置：')
###片段时间###
clip_time = int(input('输入，这个片段的持续时间为：'))
###重复率
repeat_rate = float(input('输入，重复率（0.3表示控制片段的重复率为30%）：'))
# 加速倍数
acceleration_factor = float(input('输入，几倍速播放（>1表加速，<1表减速）：'))
# 画幅大小以及比例
size = (1080, 1920)
# 逆时针旋转的度数
angle = int(input('输入，逆时针旋转的度数：'))
###加在视频上的文案###
text = int(input('输入，需要显示的文案（直接回车表示不输入广告词）：'))
files = os.listdir(path)
font = './font/new.ttf'

for file in files:
    if file.endswith('MP4') or file.endswith('mp4'):
        file_path = os.path.join(path, file)
        original_clip = VideoFileClip(file_path).rotate(angle).resize(size)

        # 加速视频
        faster_clip = original_clip.speedx(factor=acceleration_factor)
        duration = faster_clip.duration
        print(f'duration = {duration}')
        count = 0
        flag = 0
        for i in range(math.ceil(duration / clip_time)):
            if i == 0:
                start_time = 0
                end_time = clip_time
            else:
                start_time = end_time - clip_time * repeat_rate
                end_time = start_time + clip_time
            print(f'duration = {duration}, start_time = {start_time}, end_time = {end_time}')
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
                image_path1 = get_random_image(image_clip_path)
                image_clip1 = ImageClip(image_path1).set_duration(sub_clip.duration)
                image_clip1 = image_clip1.set_pos(("right", "top")).resize(height=300)
                image_path2 = get_random_image(image_clip_path)
                image_clip2 = ImageClip(image_path2).set_duration(sub_clip.duration)
                image_clip2 = image_clip2.set_pos(("right", "bottom")).resize(height=300)
                image_path3 = get_random_image(image_clip_path)
                image_clip3 = ImageClip(image_path3).set_duration(sub_clip.duration)
                image_clip3 = image_clip3.set_pos(("left", "bottom")).resize(height=300)
                sub_clip = CompositeVideoClip([sub_clip, image_clip1, image_clip2, image_clip3])
                flag = 0
            count += 1
            # 创建文本剪辑，设置字体为支持中文的字体，method为caption以便自动换行
            txt_clip = TextClip(text, fontsize=120, font=font, method='caption', color='black', size=(sub_clip.w, None))
            # 设置文本剪辑的位置和持续时间
            txt_clip = txt_clip.set_position(('center', sub_clip.h - 93 - txt_clip.h)).set_duration(sub_clip.duration)
            shadow_text = TextClip(text, fontsize=120, font=font, method='caption', color='white', size=(sub_clip.w, None))
            shadow_text = shadow_text.set_position(('center', sub_clip.h - 100 - txt_clip.h)).set_duration(sub_clip.duration)
            # 将文本剪辑叠加到视频上
            clip = CompositeVideoClip([sub_clip, txt_clip]).without_audio()
            clip = CompositeVideoClip([clip, shadow_text]).set_audio(audio)
            output_file = f"{output_path}/{file.split('.')[0]}_{count}.mp4"
            clip.write_videofile(output_file)
