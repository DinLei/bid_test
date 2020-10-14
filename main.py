#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-23
# @Author  : bading
# @File    : main.py


if __name__ == "__main__":
    from ocpx.unit_analysis import rank_log_unit_info_extract
    from ocpx.ocpx_statement import ocpx_report_forms
    from ocpx.pid_speed_extract import imp_speed_extra

    rank_log_unit_info_extract("data/rank_rt_101_1026.log",
                               unit_saved_path="result/unit_info_101_1026.csv")

    imp_speed_extra(
        "data/rank_ps_101_1026.log",
        "result/pid_speed_101_1026.csv"
    )

    ocpx_report_forms("result/unit_info_101_1026.csv",
                      set_value=1.0,
                      save_file="result/ocpx_101_1026_report.csv")
