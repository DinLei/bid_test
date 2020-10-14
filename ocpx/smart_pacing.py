#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2019-09-30
# @Author  : bading
# @File    : smart_pacing.py


"""
for (int i=1; i<ctx.num; i++) {
    float _t = ctx.bid[i] - (ctx.bid[i] - ctx.bid[i-1])/2.0/(ctx.speed[i]-ctx.speed[i-1]+0.0001) * (ctx.speed[i]-1.0);
    _t = max(_t, 0.0f);
    new_price += _t;
}
new_price /= (ctx.num-1.0+0.0001);
"""


def smart_pacing(bids, speeds):
    new_price = 0
    for i in range(1, len(bids)):
        t = bids[i] - (1/2) * (bids[i]-bids[i-1])/(speeds[i]-speeds[i-1]+0.0001) * (speeds[i]-1)
        t = max(t, 0.0)
        new_price += t
    return new_price / (len(bids)-1+0.0001)


if __name__ == "__main__":
    t_bids = [92, 97]
    t_speeds = [0.953, 0.952]
    print(smart_pacing(t_bids, t_speeds))




