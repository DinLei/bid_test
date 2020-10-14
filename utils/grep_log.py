#!/usr/bin/env python
# encoding: utf-8

# @author: ba_ding
# @contact: dinglei_1107@outlook.com
# @file: grep_log.py
# @time: 2020/9/23 15:31

import os

log_price = """
grep "%s.*Ocpx.cpp:.*(%s) adid:%s" /opt/logs/rank.log | awk -F" " '{split($5,a1,","); split($6,a2,","); split($7,a3,","); split($8,a4,","); split($9,a5,","); split($10,a6,","); split($11,a7,","); split($12,a8,","); split($13,a9,":"); split(a1[1],a11,":"); split(a2[1],a12,":"); split(a3[1],a13,":"); split(a4[1],a14,":"); split(a5[1],a15,":"); split(a6[1],a16,":"); split(a7[1],a17,":"); split(a8[1],a18,":");print $2"\\t"$1"\\t"a11[2]"\\t"a12[2]"\\t"a13[2]"\\t"a14[2]"\\t"a15[2]"\\t"a16[2]"\\t"a17[2]"\\t"a18[2]"\\t"a9[2]}'
"""

log_imp = """
grep "%s.*Ocpx.cpp:.*(Filter) \[0\]adid:%s" /opt/logs/rank.log | awk -F" " 'BEGIN{v="";}{p=substr($12,21,3); if(p!=v) {v=p; print $0;}}'|awk -F" " '{ split(substr($7,7),a,","); split($5,b,","); split($6,c,":"); split(c[2],d,","); split($12,e,":"); print $2"\\t"$1"\\t"b[1]"\\t"d[1]"\\t"d[2]"\\t"d[3]/1000000.0"\\t"a[1]"\\t"a[2]"\\t"substr(substr($8,8),0,length(substr($8,8))-1)"\\t"substr(substr($9,9),0,length(substr($9,9))-1)"\\t"substr(substr($10,13),0,length(substr($10,13))-1)"\\t"substr($11,7,5)"\\t"substr(e[2],5,3);}'
"""

modes = {
    "pid": "SmartPID",
    "opca": "SmartOcpa",
    "pace": "SmartPacing"
}


def write_file(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()


def exec_cmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def get_log_price(date, mode, units):
    units_arr = units.split(",")
    for unit in units_arr:
        mode = mode.lower()
        if not mode in modes:
            return
        mode = modes[mode]
        cmd = log_price % (date, mode, unit)
        file = "{}_{}_{}.log".format(date, mode, unit)
        text = exec_cmd(cmd)
        write_file(file, text)


def get_log_imp(date, units):
    units_arr = units.split(",")
    for unit in units_arr:
        cmd = log_imp % (date, unit)
        file = "{}_{}.log".format(date, unit)
        text = exec_cmd(cmd)
        write_file(file, text)


if __name__ == "__main__":
    import sys
    d1 = sys.argv[1]
    u1 = sys.argv[2]
    m1 = ""
    if len(sys.argv) > 3:
        m1 = sys.argv[3]
    if m1:
        get_log_price(d1, m1, u1)
    else:
        get_log_imp(d1, u1)
