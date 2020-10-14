#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-21
# @Author  : bading
# @File    : ocpx_statement.py

import pandas as pd
from utils.io_util import read_file

unit_schema = ["date", "time", "ad_id",
               "imp", "clk", "consume",
               "custo", "budget", "pbudget", "pid", "balance",
               "imp_rt", "clk_rt",
               "bid_sp", "bid_pid", "bid_lc",
               "lc_confid", "speed", "limit_update_flag"]

unit_type = [str, str, str,
             float, float, float,
             float, float, float, float, float,
             float, float, float, float, float, float, float, str]

ocpx_rf_schema = ["date", "time",
                  "imp_acc", "click_acc", "consume_acc",
                  "imp_5min", "click_5min", "consume_5min",
                  "cpc_5min", "cpm_5min", "cpc_acc", "cpm_acc",
                  "bid_sp", "sp_speed", "bid_pid", "set_value"]


def ocpx_report_forms(unit_file, set_value=1.5, save_file=None):
    result = list()
    unit_data = read_file(unit_file, types=unit_type, skip_head=True)

    last_day = ""
    last_time = ""
    last_imp = 0
    last_clk = 0
    last_consume = 0

    last_cpc_5 = 0.0
    last_cpm_5 = 0.0
    last_cpc_acc = 0.0
    last_cpm_acc = 0.0
    last_update_flag = -1

    for record in unit_data:
        sp_speed = record[17]
        update_flag = record[-1]
        if update_flag == last_update_flag:
            continue
        else:
            last_update_flag = update_flag
        tmp_record = list()
        cur_day = record[0]
        if cur_day != last_day:
            print(last_day, cur_day)
            last_cpc_5 = 0.0
            last_cpm_5 = 0.0
            last_cpc_acc = 0.0
            last_cpm_acc = 0.0
            last_imp = record[11]
            last_clk = record[12]
            last_consume = record[5]
            last_day = cur_day
            last_time = record[1]
            continue
        cur_time = record[1]
        imp_acc = record[11]
        clk_acc = record[12]
        consume_acc = record[5]
        imp_5 = imp_acc - last_imp
        clk_5 = clk_acc - last_clk
        consume_5 = consume_acc - last_consume
        last_imp = imp_acc
        last_clk = clk_acc
        last_consume = consume_acc
        if imp_5 < 0 or clk_5 < 0 or consume_5 < 0:
            continue
        tmp_record.extend([cur_day, cur_time,
                           imp_acc, clk_acc, consume_acc,
                           imp_5, clk_5, consume_5])
        if imp_5 == 0:
            cpm_5 = last_cpm_5
        else:
            cpm_5 = consume_5 / 1000.0 / imp_5
            last_cpm_5 = cpm_5
        if clk_5 == 0:
            cpc_5 = last_cpc_5
        else:
            cpc_5 = consume_5 / 1000000.0 / clk_5
            last_cpc_5 = cpc_5
        if imp_acc == 0:
            cpm_acc = last_cpm_acc
        else:
            cpm_acc = consume_acc / 1000.0 / imp_acc
            last_cpm_acc = cpm_acc
        if clk_acc == 0:
            cpc_acc = last_cpc_acc
        else:
            cpc_acc = consume_acc / 1000000.0 / clk_acc
            last_cpc_acc = cpc_acc

        tmp_record.extend([cpc_5, cpm_5, cpc_acc, cpm_acc])
        tmp_record.extend([record[13]/10.0, sp_speed, record[14]/10000.0, set_value])
        result.append(tmp_record)

        last_day = cur_day
    if set_value:
        pd.DataFrame(result, columns=ocpx_rf_schema).to_csv(save_file, index=None)


if __name__ == "__main__":
    ocpx_report_forms("../result/unit_info_101_1023.csv",
                      set_value=1.0,
                      save_file="../result/ocpx_report.csv")
