#!/bin/bash

function put_price_ctx() {
ftp -n<<!
open $1
user predict predict123
cd /predictor/
binary
prompt
put data/global_price_ctx_file.txt
put data/global_price_ctx_file.txt.touch
close
bye
!
}

function batch_put() {
file1=$1
ips=$2
hosts_line=`sed -n "/$ips/p" $file1`
hosts_str=`echo $hosts_line | sed 's/'$ips'=\([0-9\.,]*\)/\1/g'`

OLD_IFS="$IFS"
IFS=","
arr=($hosts_str)
IFS="$OLD_IFS"

sudo touch data/global_price_ctx_file.txt
sudo touch data/global_price_ctx_file.txt.touch
#遍历数组
for s in ${arr[@]}
do
put_price_ctx $s
done
}


file1=/opt/predict/predictor/release/ftp4dsp.config
key=total_list

echo "update_time: "`date "+%Y-%m-%d %H:%M:%S"`
if [ -s /opt/predict/predictor/release/data/global_price_ctx_file.txt ]; then
  batch_put $file1 $key
fi

