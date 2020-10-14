#!/bin/bash

function ftp_cmd() {
ftp -n<<!
open ossftp.suning.com
user dsprec/ocpx_online/dspCowork dsp20200715
cd /dsp/beijing
lcd `pwd`
get get_log.touch
close
bye
!
}

function ftp_cmd2() {
tar -czf logs.tar.gz logs
ftp -n<<!
open ossftp.suning.com
user dsprec/ocpx_online/dspCowork dsp20200715
cd /dsp/beijing
lcd `pwd`
put logs.tar.gz
close
bye
!
rm logs.tar.gz
rm ./logs/*
}


interval=30

cmd4price=""
cmd4imp=""
flag=0

while true
do
ftp_cmd
if [ -f ./get_log.touch ]; then
new_cmd4price=`awk 'NR==1{print}' get_log.touch`
#echo "old: "$cmd4price
#echo "new: "$new_cmd4price
if [[ -n "$new_cmd4price" ]] && [[ "$new_cmd4price" != "$cmd4price" ]]; then
flag=1
python3 get_log.py $new_cmd4price
cmd4price=$new_cmd4price
fi

new_cmd4imp=`awk 'NR==2{print}' get_log.touch`
if [[ -n "$new_cmd4imp" ]] && [[ "$new_cmd4imp" != "$cmd4imp" ]]; then
flag=$((10#$flag+1))
python3 get_log.py $new_cmd4imp
cmd4imp=$new_cmd4imp
fi

if [ $flag -gt 0 ]; then
ftp_cmd2
flag=0
fi

fi

sleep $interval
done

