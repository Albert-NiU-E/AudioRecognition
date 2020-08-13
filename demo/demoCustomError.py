class ShortInputException(Exception):  # 继承Exception
    """自定义的异常类"""

    def __init__(self, length, atleast):
        super().__init__()  # 这条语句在下文有说明
        self.length = length
        self.atleast = atleast


def main():
    try:
        s = input('请输入至少三个字符--> ')
        if len(s) < 3:  # 判断用户是否输入至少三个字符
            # raise引发一个你定义的异常
            raise ShortInputException(len(s), 3)  # raise抛出一个自定义异常类的实例的引用
    except ShortInputException as result:  # result用来接收自定义异常类的实例的引用，即相当于异常类的实例
        print('ShortInputException: 输入的长度是 %d,长度至少应是 %d' % (result.length, result.atleast))
        # 由于result也指向异常类的实例，可以通过调用result的实例属性进行输出
    else:
        print('没有异常发生.')


main()
