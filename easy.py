# -*- coding:utf-8 -*-
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, TextClip, vfx
import math
import moviepy.editor as mp
import moviepy.config as mp_config
import itertools
import os
import random
import configparser


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


def list_files_in_directory(directory, c):
    """
    返回特定后缀的文件名称
    :param directory: 需要查找的文件夹路径
    :param c: 文件扩展名
    :return: 返回所有包含此扩展名的文件名称
    """
    try:
        # 获取目录中的所有文件和文件夹
        files = [f for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(c.lower())]
        return files
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_folder_paths(directory_path):
    # 获取指定路径下的所有文件夹路径
    folder_paths = [os.path.join(directory_path, folder) for folder in os.listdir(directory_path) if
                    os.path.isdir(os.path.join(directory_path, folder))]
    return folder_paths


def create_folder(directory_path, folder_name):
    # 组合新文件夹的完整路径
    new_folder_path = os.path.join(directory_path, folder_name)
    try:
        # 创建新文件夹
        os.makedirs(new_folder_path)
        print(f"文件夹 '{folder_name}' 已成功创建于 '{directory_path}' 下。")
    except FileExistsError:
        print(f"文件夹 '{folder_name}' 已经存在于 '{directory_path}' 下。")
    except Exception as e:
        print(f"创建文件夹时发生错误: {e}")


def montage_1(clip1, clip2, clip3, clip4):
    """
        第一种拼接方式，带渐入渐出效果
    """
    final_clip = CompositeVideoClip([
        clip1,
        clip2.set_start(clip1.duration).crossfadein(0.25),
        clip3.set_start(clip1.duration + clip2.duration).crossfadein(0.25),
        clip4.set_start(clip1.duration + clip2.duration + clip3.duration).crossfadeout(0.25)
    ])
    return final_clip


def montage_2(clip1, clip2, clip3, clip4):
    """
        第二种拼接方式，直接拼接
    """
    final_clip = CompositeVideoClip([clip1, clip2, clip3, clip4])
    return final_clip


def Cut():
    # 素材库所在的文件夹位置
    input_path = config['PATHS']['FOLDER_PATH']
    path = get_folder_paths(input_path)
    # 保存的文件夹名称
    name = ["folder1", "folder2", "folder3", "folder4"]
    output = config['PATHS']['OUTPUT_PATH']
    output_path = []
    for i in range(len(name)):
        create_folder(output, name[i])
        output_path.append(os.path.join(output, name[i]))
    image_clip_path = config['PATHS']['IMAGE_PATH']
    # 片段时间
    clip_time = int(config['SETTINGS']['CLIP_TIME'])
    # 重复率
    repeat_rate = float(config['SETTINGS']['REPETITION_RATE'])
    # 加速倍数
    acceleration_factor = int(config['SETTINGS']['ACCELERATION_FACTOR'])
    # 画幅大小以及比例
    size = (int(config['SETTINGS']['SIZE_W']), int(config['SETTINGS']['SIZE_H']))
    # 逆时针旋转的度数
    angle = [int(config['SETTINGS'][f'ANGLE{i+1}']) for i in range(4)]
    # 加在视频上的文案
    text = [config['SETTINGS'][f'TEXT{i+1}'] for i in range(4)]
    font = config['PATHS']['FONT_PATH']
    # 镜头的文件夹i是镜头的游标
    for i in range(len(path)):
        # 得到一个镜头的路径，处理路径下的视频文件
        files = os.listdir(path[i])
        for file in files:
            if file.lower().endswith('mp4') | file.lower().endswith('mov'):
                # 得到视频的文件路径
                file_path = os.path.join(path[i], file)
                original_clip = VideoFileClip(file_path).without_audio().rotate(angle[i]).resize(size)
                # 给视频加倍数，得到倍速后的视频长度
                faster_clip = original_clip.speedx(factor=acceleration_factor)
                duration = faster_clip.duration
                print(f'duration = {duration}')
                count = 0
                flag = 0
                for j in range(math.ceil(duration / clip_time)):
                    if j == 0:
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
                    if text[i]:
                        # 创建文本剪辑，设置字体为支持中文的字体，method为caption以便自动换行
                        txt_clip = TextClip(text[i], fontsize=120, font=font, method='caption', color='black',
                                            size=(sub_clip.w, None))
                        # 设置文本剪辑的位置和持续时间
                        txt_clip = txt_clip.set_position(('center', sub_clip.h - 93 - txt_clip.h)).set_duration(
                            sub_clip.duration)
                        shadow_text = TextClip(text[i], fontsize=120, font=font, method='caption', color='white',
                                               size=(sub_clip.w, None))
                        shadow_text = shadow_text.set_position(('center', sub_clip.h - 100 - txt_clip.h)).set_duration(
                            sub_clip.duration)
                        # 将文本剪辑叠加到视频上
                        sub_clip = CompositeVideoClip([sub_clip, txt_clip])
                        sub_clip = CompositeVideoClip([sub_clip, shadow_text])
                        # sub_clip = CompositeVideoClip([sub_clip, txt_clip, shadow_text])
                    clip = sub_clip.without_audio()
                    output_file = f"{output_path[i]}/{file.split('.')[0]}_{count}.mp4"
                    clip.write_videofile(output_file)


def combination():
    # 保存的文件夹位置
    name = ["folder1", "folder2", "folder3", "folder4"]
    output = config['PATHS']['OUTPUT_PATH']
    output_path = []
    for i in range(len(name)):
        output_path.append(os.path.join(output, name[i]))
    music_folder = config['PATHS']['MUSIC_PATH']
    num = int(config['SETTINGS']['NUM'])
    # 只取文件名，减少内存占用
    clips_folder1 = list_files_in_directory(output_path[0], 'mp4')
    clips_folder2 = list_files_in_directory(output_path[1], 'mp4')
    clips_folder3 = list_files_in_directory(output_path[2], 'mp4')
    clips_folder4 = list_files_in_directory(output_path[3], 'mp4')
    combinations = list(itertools.product(clips_folder1, clips_folder2, clips_folder3, clips_folder4))
    selected_combinations = random.sample(combinations, min(num, len(combinations)))
    # 创建子文件夹并保存视频
    for i in range(num):
        subfolder_index = i // 100 + 1
        subfolder_path = os.path.join(output, f'成片视频_{subfolder_index}')
        os.makedirs(subfolder_path, exist_ok=True)

        clip1 = VideoFileClip(os.path.join(output_path[0], selected_combinations[i][0]))
        clip2 = VideoFileClip(os.path.join(output_path[1], selected_combinations[i][1]))
        clip3 = VideoFileClip(os.path.join(output_path[2], selected_combinations[i][2]))
        clip4 = VideoFileClip(os.path.join(output_path[3], selected_combinations[i][3]))
        video = montage_1(clip1, clip2, clip3, clip4)

        if music_folder:
            music = list_files_in_directory(music_folder, 'mp3')
            audio_path = os.path.join(music_folder, random.choice(music))
            audioclip = AudioFileClip(audio_path).subclip(0, video.duration)
            if video.duration > 15:
                video = video.without_audio().set_audio(audioclip).subclip(0, 15)
            else:
                video = video.without_audio().set_audio(audioclip).subclip(0, video.duration)
        output_file = os.path.join(subfolder_path, f'{i + 1}.MP4')

        video.write_videofile(output_file)




def start_processing():
    Cut()
    combination()


if __name__ == '__main__':
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    # 设置FFmpeg路径
    mp.ffmpeg_tools.ffmpeg_binary = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')

    # 设置 ImageMagick 的路径
    mp_config.IMAGEMAGICK_BINARY = os.path.join(os.getcwd(), 'imagemagick', 'magick.exe')
    os.environ['MAGICK_HOME'] = os.path.join(os.getcwd(), 'imagemagick')
    os.environ['PATH'] += os.pathsep + os.environ['MAGICK_HOME']
    start_processing()