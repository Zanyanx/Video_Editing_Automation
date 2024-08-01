import itertools
import random
import os
"""
    从中随机取出num个组合方式
"""
def enumerate(clips_folder1,clips_folder2,clips_folder3,clips_folder4,num):
    """
            clips_folderX:表示第X个分镜中的文件文件名称，以数字命名
            如 clips_folder1 = [1, 2, 3, 4, 5]
            num表示枚举出所有镜头的笛卡尔集之后从中随机取100个视频
    """
    # 使用 itertools.product 枚举所有可能的组合
    all_combinations = list(itertools.product(clips_folder1, clips_folder2, clips_folder3, clips_folder4))
    # 从所有组合中随机取 num 个
    random_combinations = random.sample(all_combinations,num)
    return random_combinations

def random_choosing(directory_path):
    if not os.path.isdir(directory_path):
        raise ValueError(f"{directory_path}：文件夹不存在.")
    files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if
             os.path.isfile(os.path.join(directory_path, f))]
    random_file = random.choice(files)
    return random_file

