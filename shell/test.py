from datetime import datetime
f=open('test.txt', 'a')
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
f.write("{now} test result\n".format(now=now))
f.close()
