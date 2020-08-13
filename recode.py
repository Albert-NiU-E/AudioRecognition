# coding=utf8
import wave
import pyaudio


class recode:
    def recode(self, CHUNK=44100, FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=44100, RECORD_SECONDS=20,
               WAVE_OUTPUT_FILENAME="record.wav"):
        """
        录音方法
        :param CHUNK: 缓冲区大小
        :param FORMAT: 采样大小
        :param CHANNELS:通道数
        :param RATE:采样率
        :param RECORD_SECONDS:录的时间
        :param WAVE_OUTPUT_FILENAME:输出文件路径，这里为本地文件夹
        :return:
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("...录音开始")
        print("...录音中")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  # 采样率/缓冲区大小*采样时间=chunk的数量
            data = stream.read(CHUNK)
            frames.append(data)
        print("...录音结束")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 创建二进制创建文件，若有则改为写入文件
        wf.setnchannels(CHANNELS)  # 设置通道数2
        wf.setsampwidth(p.get_sample_size(FORMAT))  # 设置format，一般为默认即可
        wf.setframerate(RATE)  # 默认采样率
        wf.writeframes(b''.join(frames))  # 加入新的frames
        wf.close()


# if __name__ == '__main__':  # 文件被作为脚本直接执行时执行以下语句，用于测试
#     a = recode()
#     a.recode(RECORD_SECONDS=20, WAVE_OUTPUT_FILENAME='test.wav')
