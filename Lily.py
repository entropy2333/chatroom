import time

t = time.localtime()
s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print(type(s), t)