#!/bin/bash

function ftp_cmd() {
ftp -n<<!
open $1
user predict predict123
cd /predictor/
binary
prompt
lcd `pwd`
$2
close
bye
!
}

function put_except_so2one_machine() {

if [ -d "data" ]; then
  cmd1="mput data/*"
  ftp_cmd $1 "$cmd1"
  echo "update $1 [data] successfully"
fi  

if [ -d "conf" ]; then
  cmd2="mput conf/*"
  ftp_cmd $1 "$cmd2"
  echo "update $1 [conf] successfully"
fi

if [ -d "lib" ]; then
  #sudo touch lib/libmtai.so.touch
  if [ -f "lib/libmtai.so.touch" ]; then
    cmd31="put lib/libmtai.so.touch"
    ftp_cmd $1 "$cmd31"  
    echo "update $1 [so.touch] successfully"
  fi
fi

}

function put_so2one_machine() {
  if [ -f "lib/libmtai.so.touch" ]; then
    ver_str=$(cat lib/libmtai.so.touch)
    ver=$((10#$ver_str))
    
    #echo "so version: lib/libmtai.so.$ver"

    if [ -f "lib/libmtai.so.$ver" ]; then
      cmd32="put lib/libmtai.so.$ver"
      ftp_cmd $1 "$cmd32"
      echo "update $1 [so] successfully"
    else
      echo "cannot find right so file!"
    fi
  fi
}

# 暂时不用，备用
function put_list_conf() {
ftp -n<<!
open $1
user predict predict123
cd /predictor/
lcd `pwd`
binary
prompt
put data/suning_features_list_business.conf
close
bye
!
}


function batch_update() {

ip_configs=$1
ip_key=$2
echo "working ips config file: "$ip_configs
hosts_line=`sed -n "/$ip_key/p" $ip_configs`
hosts_str=`echo $hosts_line | sed 's/'$ip_key'=\([0-9\.,]*\)/\1/g'`
echo "target ips: "$hosts_str"..."

#要将$hosts_str分割开，先存储旧的分隔符
OLD_IFS="$IFS"
#设置分隔符
IFS=","
#如下会自动分隔
arr=($hosts_str)
#恢复原来的分隔符
IFS="$OLD_IFS"

#遍历数组
for s in ${arr[@]}
do
put_except_so2one_machine $s
done

if [ -d "lib" ] && [ -f "lib/libmtai.so.touch" ]; then
echo "update everything except libmtai.so"
echo "we need to wait another 3min to update libmtai.so"

sleep 180

for s in ${arr[@]}
do
put_so2one_machine $s
done
fi

echo "update all machines successfully!"
}

batch_update $1 $2 
