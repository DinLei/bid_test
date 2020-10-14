#!/usr/bin/env python
# encoding: utf-8

# @author: ba_ding
# @contact: dinglei_1107@outlook.com
# @file: rank_timeuse.py
# @time: 2020/3/23 8:45 下午

import re


rule1 = r"time: (\d+) us"
unit = 1

def timeuse_statistic(file):

    timeuse_hist = {
        "total strategy time": [0, 0],
        "total feature time": [0, 0],
        "total feature factory time": [0, 0],
        "total model time": [0, 0],
        "rank_plugin total time": [0, 0]
    }

    timeuse_model = {
        "feature_parse": [0, 0],
        "feature_construct": [0, 0],
        "ctr_xfea1": [0, 0],
        "cvr_xfea1": [0, 0],
        "gds_ctr1": [0, 0],
        "gds_cvr1": [0, 0],
    }

    with open(file, "r") as fin:
        for line in fin:
            s1 = re.search(rule1, line)
            if "total strategy time" in line:
                t1 = float(s1.group(1))/unit
                timeuse_hist["total strategy time"][0] += t1
                timeuse_hist["total strategy time"][1] += 1
            if "total feature time" in line:
                t1 = float(s1.group(1))/unit
                timeuse_hist["total feature time"][0] += t1
                timeuse_hist["total feature time"][1] += 1
            if "total feature factory time" in line:
                t1 = float(s1.group(1))/unit
                timeuse_hist["total feature factory time"][0] += t1
                timeuse_hist["total feature factory time"][1] += 1
            if "total model time" in line:
                t1 = float(s1.group(1))/unit
                timeuse_hist["total model time"][0] += t1
                timeuse_hist["total model time"][1] += 1
            if "rank_plugin total time" in line:
                t1 = float(s1.group(1))/unit
                timeuse_hist["rank_plugin total time"][0] += t1
                timeuse_hist["rank_plugin total time"][1] += 1

            for key in timeuse_model.keys():
                s2 = re.search(key+r": (\d+) us", line)
                if s2:
                    t2 = float(s2.group(1)) / 1000.0
                    timeuse_model[key][0] += t2
                    timeuse_model[key][1] += 1

    print(timeuse_hist)
    print(timeuse_model)
    print()
    for k, v in timeuse_hist.items():
        print(k+": "+str(round(v[0]/v[1], 5)))
    print()
    for k, v in timeuse_model.items():
        print(k+": "+str(round(v[0]/v[1], 5)))


if __name__ == "__main__":
    import sys
    file1 = sys.argv[1]
    if len(sys.argv) > 2:
      unit = int(sys.argv[2])
    timeuse_statistic(file1)
