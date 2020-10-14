#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-14
# @Author  : bading
# @File    : unit_comparison_analysis.py

import numpy as np
import pandas as pd
from utils.io_util import read_file

unit_cols = ["solution_id", "bid_date", "bid_time",
             "tprice", "selling", "cost",
             "p_c", "s_c",
             "acc_show_flag", "acc_click_flag",
             "acc_reach_flag", "acc_app_reach_flag",
             "acc_cost"]
unit_types = [str, str, str, float, float, float,
              float, float,
              int, int, int, int, float]
result_cols = ["solution_id", "bid_date", "bid_time",
               "ave_tprice", "ave_selling", "ave_cost", "ave_acc_imp", "ave_acc_click", "ave_acc_cvr", "ave_acc_cost",
               "min_tprice", "min_selling", "min_cost", "min_acc_imp", "min_acc_click", "min_acc_cvr", "min_acc_cost",
               "max_tprice", "max_selling", "max_cost", "max_acc_imp", "max_acc_click", "max_acc_cvr", "max_acc_cost"]


def reform(unit1, u1_save_f):
    u1_data = read_file(unit1, unit_types)
    u1_df = __every_minute_analysis(u1_data)
    u1_df.to_csv(u1_save_f, index=None)


def __every_minute_analysis(data):
    one_minute_data = []
    result = []
    last_minute = ""
    last_head = list()
    for row in data:
        curr_time = ":".join(row[2].split(":")[:2])
        if last_minute and last_minute != curr_time:
            ave_v = list(np.mean(one_minute_data, axis=0))
            min_v = list(np.min(one_minute_data, axis=0))
            max_v = list(np.max(one_minute_data, axis=0))
            result.append(last_head + ave_v + min_v + max_v)
            one_minute_data.clear()
        last_minute = curr_time
        last_head = [row[0], row[1], curr_time]
        one_minute_data.append(
            [row[3], row[4], row[5], row[8], row[9], row[10], row[12]]
        )
    return pd.DataFrame(result, columns=result_cols)


if __name__ == "__main__":
    reform("../result/n_ocpx_1014_20449.csv", "../result/ocpx_every_min_1014_20449.csv")
    reform("../result/n_ocpx_1014_20662.csv", "../result/ocpx_every_min_1014_20662.csv")
