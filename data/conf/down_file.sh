#!/bin/bash

mv $1 $1".last"

ftp -n<<!
open ossftp.suning.com
user aps/dmp_ftp/jrttdmp 432fcfc6d292eecf848f63909dae5127
cd /jrtt/spider/pachong/baidu_18128421/spider/pachong/baidu_18128421
lcd `pwd`
get $1
close
bye
!
