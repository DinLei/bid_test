#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-08
# @Author  : bading
# @File    : data_gene.py

import random
import string
from utils.io_util import write2file

src = string.ascii_letters + string.digits


def data_gene4stockout_filter(num, file_path):
    count = 1
    batches = []
    for i in range(num):
        if count % 5000 == 0:
            write2file(batches, file_path)
            batches.clear()
            print("geneting {} ...".format(count))
        f1 = "".join(random.sample(src, 9))
        f2 = "".join(random.sample(string.digits, 10))
        f3 = "".join(random.sample(src, 12))
        batches.append(f1 + "_" + f2 + "_" + f3)
        count += 1
    if len(batches) > 0:
        write2file(batches, file_path)
        batches.clear()


if __name__ == "__main__":
    data_gene4stockout_filter(20000, "../data/stockout.txt")
