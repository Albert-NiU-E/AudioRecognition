# coding=utf-8
import os
import pymysql
import pyaudio
from find_marks import voice
from recode import recode


class memory:
    def __init__(self, host, port, user, passwd, db):
        """
        初始化的方法，主要是存储连接数据库的参数
        :param host:主机位置
        :param port:端口
        :param user:用户名
        :param passwd:密码
        :param db:数据库名
        """
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def addsong(self, path):
        """
        添加歌曲方法，将歌曲名和歌曲特征指纹存到数据库
        :param path: 歌曲路径
        :return:
        """
        if type(path) != str:
            raise TypeError('path need string')
        basename = os.path.basename(path)  # 返回指定path的文件名
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                   charset='utf8')
        # 创建与数据库的连接
        except:
            print('DataBase error')
            return None
        cur = conn.cursor()  # 获取操作游标
        namecount = cur.execute("select * from fp.musicdata WHERE songname = '%s'" % basename)  # 执行SQL查询，查询数据库中song_name一栏是否有basename
        # 查询新添加的歌曲是否在曲库中了
        if namecount > 0:
            print('the song has been record!')
            return None
        # 计算出来我们的音频指纹
        v = voice()  # 从find_marks模块导入的voice类
        v.loaddata(path)  # 对目标歌曲执行loaddata
        v.fft()  # 对目标歌曲执行fft
        cur.execute("insert into fp.musicdata VALUES('%s','%s')" % (basename, v.high_point.__str__()))
        # 将新歌曲的名字和指纹存到数据库中
        conn.commit()  # 向数据库提交
        cur.close()  # 关闭游标
        conn.close()  # 关闭数据库连接

    def record(self, CHUNK=44100, FORMAT=pyaudio.paInt16, CHANNELS=2, RATE=44100, RECORD_SECONDS=2,
               WAVE_OUTPUT_FILENAME="test.wav"):
        """
        录制待识别的音乐
        该函数直接由recode.py导入
        """
        a = recode()
        a.recode(CHUNK, FORMAT, CHANNELS, RATE, RECORD_SECONDS, WAVE_OUTPUT_FILENAME)

    def fp_compare(self, search_fp, match_fp):
        """
        指纹对比方法
        :param search_fp: 查询指纹
        :param match_fp: 库中指纹
        :return:最大相似值 float
        """
        if len(search_fp) > len(match_fp):
            return 0
        # 待查询指纹的长度大于与库中对比指纹的长度，则为不匹配
        max_similar = 0  # 初始最大相似数为0
        search_fp_len = len(search_fp)  # 得到待查询指纹的长度
        match_fp_len = len(match_fp)  # 得到库中与之对比的指纹的长度
        for i in range(match_fp_len - search_fp_len):
            temp = 0
            for j in range(search_fp_len):
                if match_fp[i + j] == search_fp[j]:  # 得到整段指纹序列中重合的次数
                    temp += 1
            if temp > max_similar:
                max_similar = temp
        # 得到与库中指纹与待查询指纹对比最大的相似值
        return max_similar

    def search(self, path):
        """
        搜索方法，输入为文件路径
        :param path: 待检索文件路径
        :return: 按照相似度排序后的列表，元素类型为tuple，二元组，歌曲名和相似匹配值
        """
        # 先计算出来我们的音频指纹
        v = voice()
        v.loaddata(path)
        v.fft()
        # 尝试连接数据库
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                   charset='utf8')
        except:
            raise IOError('DataBase error')
        cur = conn.cursor()  # 获取操作游标
        cur.execute("SELECT * FROM fp.musicdata")  # 选择目标数据库
        result = cur.fetchall()  # 获取所有的记录列表
        compare_res = []  # 存放对比结果
        # 将待查询指纹与库中所有指纹进行对比
        for i in result:
            compare_res.append((self.fp_compare(v.high_point[:-1], eval(i[1])), i[0]))
        compare_res.sort(reverse=True)  # 按照相似度降序排列
        cur.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        print(compare_res)  # 输出与曲库中歌曲的相似度
        return compare_res
