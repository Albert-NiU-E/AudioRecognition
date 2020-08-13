# coding=utf8
import os
import re
import wave
import numpy as np
import pyaudio


class voice:
    def loaddata(self, filepath):
        """
        :param filepath: 文件路径，为wav文件
        :return: 如果无异常则返回True，如果有异常退出并返回False
        self.wave_data内储存着多通道的音频数据，其中self.wave_data[0]代表第一通道
        具体有几通道，看self.nchannels
        """

        p1 = re.compile('\.wav')  # 找到目标路径中的wav格式的文件
        if p1.findall(filepath) is None:
            raise IOError('the suffix of file must be .wav')  # 错误报告：目标路径中找不到wav格式的文件
        try:
            f = wave.open(filepath, 'rb')  # 读取文件
            params = f.getparams()
            self.nchannels, self.sampwidth, self.framerate, self.nframes = params[:4]
            str_data = f.readframes(self.nframes)
            self.wave_data = np.fromstring(str_data, dtype=np.short)
            self.wave_data.shape = -1, self.sampwidth
            self.wave_data = self.wave_data.T
            f.close()
            self.name = os.path.basename(filepath)  # 记录下文件名
            return True
        except:
            raise IOError('File Error')  # 错误报告：读取文件错误

    def fft(self, frames=20):
        """
        整体指纹提取的核心方法，将整个音频分块后分别对每块进行傅里叶变换，之后分子带抽取高能量点的下标
        :param frames: frames是指定每秒钟分块数
        :return:
        """
        block = []  # 存放分块后的音频数据
        fft_blocks = []  # 存放fft后的结果
        self.high_point = []  # 存放高能量的下标
        blocks_size = int(self.framerate / frames)  # block_size为每一块的frame数量
        for i in range(0, len(self.wave_data[0]) - blocks_size, blocks_size):
            block.append(self.wave_data[0][i:i + blocks_size])  # 对音频分块
            fft_blocks.append(np.abs(np.fft.fft(self.wave_data[0][i:i + blocks_size])))  # 对各分块fft处理
            self.high_point.append((np.argmax(fft_blocks[-1][:30]),  # 找到(0,30),(30,60),(60,100)三个区间的高能量下标
                                    np.argmax(fft_blocks[-1][30:60]) + 30,
                                    np.argmax(fft_blocks[-1][60:100]) + 60,
                                    # np.argmax(fft_blocks[-1][100:200]) + 100,
                                    ))

    def play(self, filepath):
        """
        音频播放方法
        :param filepath:文件路径
        :return:
        """
        chunk = 1024
        wf = wave.open(filepath, 'rb')
        p = pyaudio.PyAudio()
        # 打开声音输出流
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=False)
        # 写声音输出流进行播放
        while True:
            data = wf.readframes(chunk)
            if data == "":
                break
            stream.write(data)
        stream.close()
        p.terminate()


# if __name__ == '__main__':  # 文件被作为脚本直接执行时执行以下语句，用于测试
#     p = voice()
#     p.play('test.wav')
#     print(p.name)
