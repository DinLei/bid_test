#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-11
# @Author  : bading
# @File    : data_prepare.py

from utils.io_util import write2file


def ocpx_hive_data_prepare(data_file, save_file):
    cols = ["solution_id", "dpa_gds_cd", "bid_date", "bid_time",
            "tprice", "selling", "cost",
            "p_c", "s_c",
            "acc_show_flag", "acc_click_flag",
            "acc_reach_flag", "acc_app_reach_flag",
            "acc_cost"]
    result = []
    counter = 0
    write2file([",".join(cols)], save_file, True)
    with open(data_file, "r") as fin:
        acc_show = 0
        acc_click = 0
        acc_reach = 0
        acc_app_reach = 0
        acc_consume = 0
        for line in fin:
            line = line.strip()
            if counter % 500 == 0:
                write2file(result, save_file)
                result.clear()
            fields = line.split(",")
            assert len(fields) == 14
            tmp = list()
            tmp.append(fields[1])
            tmp.append(fields[2])
            tmp.append(fields[3])
            tmp.append(fields[4])

            t_price = float(fields[5])
            selling = float(fields[6])
            cost = float(fields[7])
            p_c = t_price/cost  # 8
            s_c = selling/cost  # 9
            acc_show += int(fields[10])
            acc_click += int(fields[11])
            acc_reach += int(fields[12])
            acc_app_reach += int(fields[13])
            acc_consume += cost
            tmp.append(t_price)
            tmp.append(selling)
            tmp.append(cost)
            tmp.append(p_c)
            tmp.append(s_c)
            tmp.append(acc_show)
            tmp.append(acc_click)
            tmp.append(acc_reach)
            tmp.append(acc_app_reach)
            tmp.append(acc_consume)

            result.append(",".join([str(x) for x in tmp]))
            counter += 1
        if len(result) > 0:
            write2file(result, save_file)
            result.clear()


if __name__ == "__main__":
    file = "../data/ocpx_1014_20662.csv"
    ocpx_hive_data_prepare(file, "../result/n_ocpx_1014_20662.csv")
    # file = "../data/ocpx_1014_20449.csv"
    # ocpx_hive_data_prepare(file, "../result/n_ocpx_1014_20449.csv")
