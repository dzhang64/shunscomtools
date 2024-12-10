import logging
from logging import Logger


class MyLogging(Logger):

    def __init__(self, file):
        # 设置日志的名字、日志的收集级别
        super().__init__("test_api", logging.DEBUG)

        # 自定义日志格式(Formatter), 实例化一个日志格式类
        fmt_str = '%(asctime)s - %(filename)s - line:%(lineno)d - %(levelname)s - %(message)s -%(process)s'
        formatter = logging.Formatter(fmt_str)

        # 实例化控制台渠道(StreamHandle)
        sh = logging.StreamHandler()
        # 设置控制台输出的日志级别
        sh.setLevel(logging.DEBUG)
        # 设置渠道当中的日志显示格式
        sh.setFormatter(formatter)
        # 追加写入文件a ，设置utf-8编码防止中文写入乱码
        test_log = logging.FileHandler(file, 'a', encoding='utf-8')
        # 向文件输出的日志级别
        test_log.setLevel(logging.DEBUG)
        test_log.setFormatter(formatter)
        # 将渠道与日志收集器绑定起来
        self.addHandler(sh)
        self.addHandler(test_log)
        sh.close()


# 实例化MyLogger对象，在其他文件直接使用log就能调用


if __name__ == '__main__':
    log = MyLogging(r'log.log')
    log.error("this is a error log")
    log.info("this is a info log")
    log.debug("this is a debug log")
    log.warning("this is a warning log")
