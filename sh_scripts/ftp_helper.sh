#!/bin/bash

time=$(date "+%m%d")
new_log_name="rank_10_"$time".log"
cp ./rank.log ./$new_log_name

ftp -n<<!
open ossftp.suning.com
user aps/dmp_ftp/jrttdmp 432fcfc6d292eecf848f63909dae5127
cd /jrtt/spider/pachong/baidu_18128421/spider/pachong/baidu_18128421
lcd `pwd`
put $new_log_name
close
bye
!
