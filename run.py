from behave.__main__ import main as behave_main
import threading
import sys
from random import randint
from time import sleep
from glob import glob
import os
 
def dostuff(path, flags):
    slept = randint(10, 150) / 1000
    sleep(slept)
    print('slept {} for thread with path {} and flags {}'.format(slept, path, flags))


def runner(feat):
    # come argomenti puoi passare l'elenco dei path che behave deve eseguire
    thr = []
    for role in feat:
        for mod in feat[role]:        
            # previous versions when we had't Allure and we worked just with paths
            # t = threading.Thread(target=behave_main, args=([x, '-t @run', '-k'],))
            # t = threading.Thread(target=behave_main, args=(['features\\'+x, '-f allure_behave.formatter:AllureFormatter', '-orep\\'+p[0]],))
            t = threading.Thread(target=behave_main, args=([feat[role][mod][0], '-f allure_behave.formatter:AllureFormatter', feat[role][mod][1]],))
            # example to understand what we are doing
            # t = threading.Thread(target=dostuff, args=(feat[role][mod][0], ['-t @run', feat[role][mod][1]]))
            t.start()
            thr.append(t)
    return thr


if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print("Please insert at leas one path\nUsage: run.py role1<\module1> <role2<\module2>> <...> <roleN<\moduleN>>")
        sys.exit(1)
    ft = {}
    for x in sys.argv[1:]:
        p = os.path.split(x)
        role = p[0] if p[0] != '' else p[1]
        print('Got role {} from path {}'.format(role, p))
        if role not in ft:
            ft[role] = {}

        if p[0] != '':
            # we have a role or a functionality or a single feature file
            ft[role][p[1]] = [os.path.join('features', x), os.path.join('-oreport', role)]
        else:
            dirs = [name for name in os.listdir(os.path.join('features', role)) if os.path.isdir(os.path.join('features', role, name))]
            for module in dirs:
                ft[role][module] = [os.path.join('features', role, module), os.path.join('-oreport', role)]
    thrs = runner(ft)
    # we may want to wait and check every thread but is not so easy :)
    # I'll write here a starting point
    for i in range(len(thrs)):
        thrs[i].join()
    print('All our {} thread completed succesfully!'.format(len(thrs)))
