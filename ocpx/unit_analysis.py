#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-09-30
# @Author  : bading
# @File    : unit_analysis.py

import re
import pandas as pd

unit_info_pattern1 = re.compile("adid:(\d+), rt_limit:(.*?), pvclk:([\d,.]+), bid_sp:([-.\d]+), bid_pid:([-.\d]+), bid_lc:([-.\d]+), lc_confid:([-.\d]+), speed=([-.\d]+),")
unit_info_pattern2 = re.compile("adid:(\d+), rt_limit:(.*?), pvclk:([\d,.]+), bid_sp:([-.\d]+), bid_pid:([-.\d]+), bid_lc:([-.\d]+), lc_confid:([-.\d]+), speed=([-.\d]+), limit_update_flag:([/\d]+),")

unit_info_pid_pattern = re.compile("adid:(\d+), pre_bid:([-.\d]+), delta_price:([-.\d]+), new_bid:([-.\d]+), set_value:([-.\d]+), act_value:([-.\d]+)")
item_info_pattern = re.compile("item_id:(\d+), bid_sp:([-.\d]+), bid_pid:([-.\d]+), bid_lc:([-.\d]+)")

unit_schema = ["date", "time", "ad_id",
               "imp", "clk", "consume",
               "custo", "budget", "pbudget", "pid", "balance",
               "imp_rt", "clk_rt",
               "bid_sp", "bid_pid", "bid_lc",
               "lc_confid", "speed", "limit_update_flag"]

unit_pid_schema = ["date", "time",
                   "ad_id", "pre_bid", "delta_price",
                   "new_bid", "set_value", "actual_value"]

item_schema = ["date", "time", "ad_id", "item_id",
               "item_bid_sp", "item_bid_pid", "item_bid_lc",
               "unit_bid_sp", "unit_bid_pid", "unit_bid_lc"]


"""
测试单元id: 20447,20446
"""


def rank_log_unit_info_extract(
        file, target_units=[],
        unit_saved_path=None, item_saved_path=None, unit_pid_path=None):
    unit_results = list()
    unit_pid_res = list()
    item_results = list()
    unit_index = None
    with open(file, "r") as fin:
        last_unit_bit_info = None
        for line in fin:
            time_str = line[:19]
            date_v, time_v = time_str.split(" ")
            unit_pid_obj = unit_info_pid_pattern.search(line)
            if unit_pid_obj:
                unit_pid_tmp = []
                unit_pid_info = unit_pid_obj.groups()
                unit_pid_tmp.extend([date_v, time_v])
                unit_pid_tmp.append(unit_pid_info[0])
                unit_pid_tmp.append(float(unit_pid_info[1]))
                unit_pid_tmp.append(float(unit_pid_info[2]))
                unit_pid_tmp.append(float(unit_pid_info[3]))
                unit_pid_tmp.append(float(unit_pid_info[4]))
                unit_pid_tmp.append(float(unit_pid_info[5]))
                unit_pid_res.append(unit_pid_tmp)
            unit_obj = unit_info_pattern2.search(line)
            if not unit_obj:
                unit_obj = unit_info_pattern1.search(line)
            if unit_obj:
                unit_info = list(unit_obj.groups())
                if len(unit_info) == 8:
                    unit_info.append("-1")
                assert len(unit_info) == 9
                unit_index = unit_info[0]
                if target_units and (unit_index not in target_units):
                    continue
                unit_bid_tmp = list()
                unit_bid_tmp.extend([date_v, time_v])
                unit_bid_tmp.append(unit_info[0])
                unit_bid_tmp.extend([float(x) for x in unit_info[1].split(",")])
                unit_bid_tmp.extend([float(x) for x in unit_info[2].split(",")])
                unit_bid_tmp.append(float(unit_info[3]))
                unit_bid_tmp.append(float(unit_info[4]))
                unit_bid_tmp.append(float(unit_info[5]))
                unit_bid_tmp.append(float(unit_info[6]))
                unit_bid_tmp.append(float(unit_info[7]))
                unit_bid_tmp.append(str(unit_info[8]))
                last_unit_bit_info = unit_bid_tmp
                unit_results.append(unit_bid_tmp)
            else:
                item_obj = item_info_pattern.search(line)
                if item_obj and last_unit_bit_info:
                    item_info = item_obj.groups()
                    assert len(item_info) == 4
                    tmp = list()
                    tmp.extend([date_v, time_v])
                    tmp.append(unit_index)
                    tmp.append(item_info[0])
                    tmp.append(float(item_info[1]))
                    tmp.append(float(item_info[2]))
                    tmp.append(float(item_info[3]))
                    tmp.append(float(last_unit_bit_info[13]))
                    tmp.append(float(last_unit_bit_info[14]))
                    tmp.append(float(last_unit_bit_info[15]))
                    item_results.append(tmp)

    if unit_saved_path:
        unit_df = pd.DataFrame(unit_results, columns=unit_schema)
        unit_df.to_csv(unit_saved_path, index=None)
    if item_saved_path:
        item_df = pd.DataFrame(item_results, columns=item_schema)
        item_df.to_csv(item_saved_path, index=None)
    if len(unit_pid_res) > 0 and unit_pid_path:
        unit_pid_df = pd.DataFrame(unit_pid_res, columns=unit_pid_schema)
        unit_pid_df.to_csv(unit_pid_path, index=None)


if __name__ == "__main__":
    rank_log_unit_info_extract("../data/rank_101_1023.log",
                               unit_saved_path="../result/unit_info_101_1023.csv")
                               # item_saved_path="../result/item_info_101_1021.csv")
                               # unit_pid_path="../result/unit_pid_info_101_1018.csv")

    # rank_log_unit_info_extract("../data/rank_102_1018.log",
    #                            unit_saved_path="../result/unit_info_102_1018.csv",
    #                            item_saved_path="../result/item_info_102_1018.csv",
    #                            unit_pid_path="../result/unit_pid_info_102_1018.csv")
