import os
from sys import platform


def trouble_pars():
    # You shouldn't need to change this variable so long as you've got
    # your source code in the original src folder. If you do, please comment
    # it here.
    rootdir = '../log/trouble/'

    # a check to see which platform you're using. These commands will
    # delete your existing normalized images before create a new set.
    # if (platform == "darwin" or platform == "linux" or platform == "linux2"):
    #    cmd1 = ("rm " + rootdir + "normalized_images/crater/*.jpg")
    #    cmd2 = ("rm " + rootdir + "normalized_images/non-crater/*.jpg")
    #    os.system(cmd1)
    # elif (platform == "win32" or platform == "cygwin"):
    #    cmd1 = ("del /f " + rootdir + "normalized_images/crater/*.jpg")
    #    cmd2 = ("del /f " + rootdir + "normalized_images/non-crater/*.jpg")
    #    os.system(cmd1)

    fns = {}
    fps = {}

    trans_table = dict.fromkeys(map(ord, '[],'), None)

    for root, dirs, files in os.walk(rootdir):

        # Skip hidden directories and files.
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        for file in files:
            with open(rootdir + file, 'r') as nthfile:
                for line in nthfile:
                    sets = line.split(',')
                    fns_set = sets[0].translate(trans_table)
                    for i in range(1, len(sets)):
                        fns_set += sets[i].translate(trans_table)
                    # print(fns_set)
                    fns_set = fns_set.split()
                    for name in fns_set:
                        if name in fns.keys():
                            fns[name] = fns[name] + 1
                        else:
                            fns[name] = 1
    for name in fns:
        if(fns[name] > 0):
            print('{0} == {1}'.format(name, fns[name]))

if __name__ == '__main__':
    trouble_pars()
