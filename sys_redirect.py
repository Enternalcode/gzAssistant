import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if not sys.stdout:
    class FakeStdOut:
        def __init__(self, filename="sys.log"):
            self.log = open(filename, "a", encoding='utf-8')

        def write(self, message):
            # try:
            #     self.log.write(message)
            # except UnicodeEncodeError as e:
            #     new_message = message.encode('utf-8', 'ignore').decode('utf-8')
            #     self.log.write(new_message)
            
            # 系统语言引起，为兼容，去掉
            # https://blog.csdn.net/xavier_muse/article/details/98853513
            pass

        def flush(self):
            pass

        def isatty(self):
            return True

    sys.stdout = FakeStdOut()
