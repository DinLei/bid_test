#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-10-15
# @Author  : bading
# @File    : pid_simulator.py

kp = 0.78
ki = 0.05
kd = 0.35
pid_err_hist = [0, 0, 0]
last_pid = 21371


def pid_core(set_val, act_val):
    pid_err_hist[0] = set_val - act_val
    print("curr pid err hist: {} ...".format(pid_err_hist))
    inc = kp * pid_err_hist[0] - ki * pid_err_hist[1] + kd * pid_err_hist[2]
    pid_err_hist[2] = pid_err_hist[1]
    pid_err_hist[1] = pid_err_hist[0]
    return inc


def get_new_price(consume, click):
    act_val = consume / 1000000.0 / (click + 0.0001) * 10000
    pid_inc = pid_core(10000, act_val)
    if abs(pid_inc) >= 30000:
        pid_inc = pid_inc/abs(pid_inc)*30000
    curr_pid = last_pid + pid_inc
    print("curr cpc: {}, last pid: {}, curr pid inc: {}, curr pid: {} ...".format(
        act_val, last_pid, pid_inc, curr_pid))
    return curr_pid


if __name__ == "__main__":
    from utils.io_util import read_file
    # rt_hist = [(7834500, 1084, 6), (16241410, 1649, 8), (24330900, 2234, 16)]
    rt_hist = read_file("../data/pid_test", [int, int, int], False)
    counter = 0
    for tmp_rt in rt_hist:
        counter += 1
        if counter == 20:
            # break
            last_pid = 20
            print("=======================================")
        last_pid = get_new_price(tmp_rt[2], tmp_rt[1])
        # print(last_pid)
