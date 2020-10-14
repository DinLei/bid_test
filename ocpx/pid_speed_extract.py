#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-23
# @Author  : bading
# @File    : pid_speed_extract.py

import re
import pandas as pd

imp_speed_pattern = re.compile("pre_bid_adv:([-.\d]+), pre_bid:([-.\d]+), delta_price:([-.\d]+), new_bid:([-.\d]+), set_value:([-.\d]+), act_value:([-.\d]+), speed:([-.\d]+)")

pid_speed_schema = ["date", "time",
                    "pre_bid_adv", "pre_bid", "delta_price", "new_bid",
                    "set_value", "act_value", "speed"]


def imp_speed_extra(file, save_file):
    res = list()
    with open(file, "r") as fin:
        for line in fin:
            time_str = line[:19]
            date_v, time_v = time_str.split(" ")
            ps_obj = imp_speed_pattern.search(line)
            if ps_obj:
                ps_gp = ps_obj.groups()
                tmp = [float(x)/10000 for x in ps_gp[:-1]]
                tmp.append(float(ps_gp[-1]))
                res.append([date_v, time_v] + tmp)
    if save_file:
        pd.DataFrame(res, columns=pid_speed_schema).to_csv(save_file)


if __name__ == "__main__":
    imp_speed_extra(
        "../data/rank_ps_101_1026.log",
        "../result/pid_speed_101_1026.csv"
    )

