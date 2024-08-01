from moviepy.editor import *
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from enumerate import *
import os
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
def montage_1(clip1,clip2,clip3,clip4):
    final_clip = CompositeVideoClip([clip1, clip2.set_start(clip1.duration).crossfadein(0.25), clip3.set_start(clip1.duration+clip2.duration).crossfadein(0.25), clip4.set_start(clip1.duration+clip2.duration+clip3.duration).crossfadeout(0.25)])
    return final_clip
def montage_2(clip1,clip2,clip3,clip4):
    final_clip = CompositeVideoClip([clip1, clip2, clip3, clip4])
    return final_clip

print('请按照提示的文字输入内容，回车表示输入完成')
# 假设每个文件夹中的视频素材文件名
folder1 = input('请输入第一个片段的文件夹路径：')
clips_folder1 = list_files_in_directory(folder1)
folder2 = input('请输入第二个片段的文件夹路径：')
clips_folder2 = list_files_in_directory(folder2)
folder3 = input('请输入第三个片段的文件夹路径:')
clips_folder3 = list_files_in_directory(folder3)
folder4 = input('请输入第四个片段的文件夹路径:')
clips_folder4 = list_files_in_directory(folder4)
output_path = input('请输入输出视频的文件夹路径:')
###从所有排列组合方式中随机取50种
num = int(input('希望得到的视频条数：'))
combination = enumerate(clips_folder1,clips_folder2,clips_folder3,clips_folder4,num)
for i in range(num):
    path1 = os.path.join(folder1,combination[i][0])
    path2 = os.path.join(folder2,combination[i][1])
    path3 = os.path.join(folder3,combination[i][2])
    path4 = os.path.join(folder4,combination[i][3])
    clip1 = VideoFileClip(path1)
    clip2 = VideoFileClip(path2)
    clip3 = VideoFileClip(path3)
    clip4 = VideoFileClip(path4)
    vedio = montage_1(clip1,clip2,clip3,clip4)
    output= output_path + '/' + str(i+1) + '.MP4'
    vedio.write_videofile(output)


