#!/usr/bin/bash

date1=`date +%Y-%m-%d`
time1=`date +%H:%m`

sudo grep "$date1.*Ocpx.*" /opt/logs/rank.log > ${date1}_rank.log

ftp -n<<!
open ossftp.suning.com
user dsprec/ocpx_online/dspCowork dsp20200715
cd /dsp/beijing
lcd `pwd`
put ${date1}_rank.log
close
bye
!

sudo rm -f ${date1}_rank.log
#sudo echo > rank.log
