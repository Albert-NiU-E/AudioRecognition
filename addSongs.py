# coding=utf-8
import os
from add_and_search import memory


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件


if __name__ == '__main__':
    file_name('./localSongs')

# if __name__ == '__main__':
#     sss = memory('localhost', 3306, 'root', 'ALBERTniu314', 'fp')
#     sss.addsong('songsDataWav/『天気の子』のテーマ.wav')
#     sss.addsong('songsDataWav/Shape_of_You.wav')
