#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-15
# @Author  : bading
# @File    : other_utils.py


def recall_item_common(item_info, n_ocpx):
    items1 = []
    items2 = []
    with open(item_info, "r") as fin1:
        for line in fin1:
            fields = line.split(",")
            items1.append(fields[3] + "_" + "")
    print("{}:{}".format(item_info, len(items1)))
    print(items1[:5])
    with open(n_ocpx, "r") as fin2:
        for line in fin2:
            fields = line.split(",")
            items2.append(fields[1] + "_" + "")
    print("{}:{}".format(n_ocpx, len(set(items2))))
    print(items2[:5])
    common_part = set(items1).intersection(items2)
    print("common part: {}".format(len(set(common_part))))
    return list(common_part)


if __name__ == "__main__":
    from utils.io_util import write2file
    cp = recall_item_common("../result/item_info_10_1015.csv",
                            "../result/n_ocpx_1014_20662.csv")
    if len(cp) > 0:
        write2file(cp, "../result/common_part.txt")

