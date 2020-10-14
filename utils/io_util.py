#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-08
# @Author  : bading
# @File    : io_util.py


def write2file(data, file, is_first_time=False):
    if is_first_time:
        with open(file, "w") as fout:
            for ele in data:
                fout.write(ele)
                fout.write("\n")
    else:
        with open(file, "a") as fout:
            for ele in data:
                fout.write(ele)
                fout.write("\n")


def read_file(file, types=None, skip_head=True):
    res = list()
    with open(file, "r") as fin:
        for line in fin:
            if skip_head:
                skip_head = False
                continue
            fields = line.split(",")
            if types:
                assert len(types) == len(fields)
                fields = [types[i](fields[i]) for i in range(len(fields))]
            res.append(fields)
    return res
