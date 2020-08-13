import os
import pymysql
import pyaudio
from find_marks import voice
from recode import recode
from add_and_search import memory
from mp3ToWave import trans
from addSongs import file_name

if __name__ == '__main__':
    sss = memory('localhost', 3306, 'root', 'ALBERTniu314', 'fp')  # 连接数据库，做好运行准备
    print("数据库已经连接，请输入你想进行的操作")
    while True:
        print("1--> addsongs to database")
        print("2--> record and search songs")
        print("0--> exit")
        choice_str = input("")
        choice = int(choice_str)
        if choice == 1:
            try:
                print("本地存储下的mp3文件目录：")
                file_name('./localSongs')
                inputName = input("你希望导入哪一首？(仅乐曲名)")
                trans('localSongs/%s.mp3' % inputName, inputName)  # 格式转换
                sss.addsong('songsDataWav/%s.wav' % inputName)
                print("数据库已经成功导入:%s.wav" % inputName)
            except:
                print("文件名输入错误，请验证！")

        elif choice == 2:
            sss.record(RECORD_SECONDS=5, WAVE_OUTPUT_FILENAME='test.wav')
            sss.search('test.wav')
        elif choice == 0:
            print("感谢使用！")
            break
        else:
            print("Invalid Input!")
