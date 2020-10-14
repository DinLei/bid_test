# -*- coding: utf-8 -*-

import argparse
import shutil
import os, sys, json, itertools
import time, re

class PriceCtx:
  def __init__(self):
    self.adid = 0
    self.bid = 0
    self.bid_cpc = 0
    self.bid_cpa = 0
    self.cnt = 0
  
  def __str__(self):
    return "adid:{},bid:{},bid_cpc:{},bid_cpa:{},cnt:{}".format(self.adid, self.bid, self.bid_cpc, self.bid_cpa, self.cnt)

def handle(adlist, file):
  with open(file, 'r') as fp:
    for line in fp:
      if not line:
        break
  #    print(line)
      arr = re.split(';', line.strip())
      ts = int(arr[0])
      now = time.time()
      if (now-ts) > 10*60:
        continue

      for k in range(1, len(arr)):
        l2 = arr[k]
        tokens = re.split('\t| |,', l2.strip())
  #      print(tokens)
        if len(tokens) < 5:
          continue

        adid = int(tokens[0])
        cnt = int(tokens[1])
        bid = float(tokens[2])
        bid_cpc = float(tokens[3])
        bid_cpa = float(tokens[4])

        if not adlist.has_key(adid):
          adlist[adid] = PriceCtx()
        ad = adlist[adid]
        ad.bid += bid
        ad.bid_cpc += bid_cpc
        ad.bid_cpa += bid_cpa
        ad.cnt += cnt

def mix(dest_dir, out_file):
  adlist = {}

  for root, dirs, files in os.walk(dest_dir):
    for file in files:
      #print("handle %s" % (root+'/'+file))
      handle(adlist, root+'/'+file)  
  
#  for k, v in adlist.items():
#    print("key:{}, val:{}".format(k, v))

  out_fp = open(out_file, 'w')
  for adid,ctx in adlist.items():
    out_fp.writelines('%d,%d,%.2f,%.2f,%.2f\n' % (adid, ctx.cnt, ctx.bid/ctx.cnt, ctx.bid_cpc/ctx.cnt, ctx.bid_cpa/ctx.cnt))
  out_fp.close()

if __name__ == '__main__':
  mix('tmp/', sys.argv[1])

