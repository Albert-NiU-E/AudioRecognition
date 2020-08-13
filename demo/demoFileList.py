import fnmatch
import os
import pandas as pd
import numpy as np
import sys

InputStra = sys.argv[1]
InputStrb = sys.argv[2]


def ReadSaveAddr(Stra, Strb):
    print("Read :", Stra, Strb)
    a_list = fnmatch.filter(os.listdir(Stra), Strb)
    print("Find = ", len(a_list))
    df = pd.DataFrame(np.arange(len(a_list)).reshape((len(a_list), 1)), columns=['Addr'])
    df.Addr = a_list
    # print(df.head())
    df.to_csv('Get.lst', columns=['Addr'], index=False, header=False)
    print("Write To Get.lst !")

ReadSaveAddr(InputStra, InputStrb)
