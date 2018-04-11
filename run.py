from behave.__main__ import main as behave_main
import threading
import sys
from random import randint
from time import sleep
 
def dostuff(path, flags):
    slept = randint(10, 150) / 1000
    sleep(slept)
    print('slept {} for thread with path {} and flags {}'.format(slept, path, flags))


def runner(argv):
    # come argomenti puoi passare l'elenco dei path che behave deve eseguire
    thr = []
    for x in argv[1:]:
        p = x.split('\\')
        # previous versions when we had't Allure and we worked just with paths
        # t = threading.Thread(target=behave_main, args=([x, '-t @run', '-k'],))
        t = threading.Thread(target=behave_main, args=(['features\\'+x, '-f allure_behave.formatter:AllureFormatter', '-orep\\'+p[0]],))
        # example to understand what we are doing
        # t = threading.Thread(target=dostuff, args=(x, ['-t @run', '-k']))
        t.start()
        thr.append(t)
    return thr


if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print("Please insert at leas one path\nUsage: run.py role1<\module1> <role2<\module2>> <...> <roleN<\moduleN>>")
        sys.exit(1)
    thrs = runner(sys.argv)
    # we may want to wait and check every thread but is not so easy :)
    # I'll write here a starting point
    for i in range(len(thrs)):
        thrs[i].join()
