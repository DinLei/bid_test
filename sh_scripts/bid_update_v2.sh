#!/bin/bash

function get_price_ctx() {
ftp -n<<!
open $1
user predict predict123
cd /predictor/
binary
prompt
get tmp/price_ctx_file.txt
close
bye
!

curr_time=`date +%s`
sudo mv tmp/price_ctx_file.txt tmp/${1}_price_ctx_${curr_time}
}

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

function batch_get() {
file1=$1
ips=$2
#echo "ftp config file: "$file1
hosts_line=`sed -n "/$ips/p" $file1`
hosts_str=`echo $hosts_line | sed 's/'$ips'=\([0-9\.,]*\)/\1/g'`
#echo "target ips: "$hosts_str"..."

OLD_IFS="$IFS"
IFS=","
arr=($hosts_str)
IFS="$OLD_IFS"

#遍历数组
for s in ${arr[@]}
do
get_price_ctx $s
done
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
if [ ! -d "tmp" ]; 
then
  mkdir tmp
else 
  sudo rm -rf /opt/predict/predictor/release/tmp/* 
fi
batch_get $file1 $key
sudo python /opt/predict/predictor/release/mix_v2.py /opt/predict/predictor/release/data/global_price_ctx_file.txt
if [ -s /opt/predict/predictor/release/data/global_price_ctx_file.txt ]; then
  batch_put $file1 $key
fi

