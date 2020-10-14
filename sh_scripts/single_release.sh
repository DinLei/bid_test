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

function copy() {
#  cp lib ./last_version -Rf
#  cp data ./last_version -Rf
#  cp conf ./last_version -Rf

  cd ../build/
  
  ver_str=$(cat ../release/lib/libmtai.so.touch)
  ver=$((10#$ver_str+1))
#  ver=0
#  cp libranking.so ../release/lib/ -Rf
  cp libmtai.so ../release/lib/libmtai.so.$ver -Rf
  echo "$ver" > ../release/lib/libmtai.so.touch
#  cp test ../release/lib/ -Rf

  #cp ../data/*.txt ../release/data/
  #cp ../data/*.conf ../release/data/
#  cp ../data/fm.model ../release/data/
#  cp ../data/suning_features.conf ../release/data/
#  cp ../data/suning_features_list.conf ../release/data/
  #cp ../conf/graph_suning_dsp.conf ../release/conf/

  # 全局搜索替换路径
  #cp ../conf/libranking.so.conf ../release/conf/
  #sed -i "s/\/opt\/predict\/predictor\/dsp_predictor/\/opt\/predict\/predictor/g" ../release/conf/libranking.so.conf

  #cp ../conf/log4cpp.conf ../release/conf/
  #sed -i "s/\/opt\/predict\/predictor\/dsp_predictor\/build\/rank.log/\/opt\/logs\/rank.log/g" ../release/conf/log4cpp.conf
#  sed -i "s/\/opt\/predict\/predictor\/dsp_predictor\/data/\/opt\/predict\/predictor\/data/g" ../release/data/suning_features.conf

  cd -
}

function put_so() {
  ver_str=$(cat lib/libmtai.so.touch)
  ver=$((10#$ver_str))

  cmd10="put lib/libmtai.so.$ver"
  ftp_cmd $1 "$cmd10"
}

function update_so() {
  touch lib/libmtai.so.touch
  cmd20="put lib/libmtai.so.touch"
  ftp_cmd $1 "$cmd20"
}

function put_else() {
#  cmd1="put data/calibrate.txt"
#  cmd1="put conf/libranking.so.conf"
#  ftp_cmd $1 "$cmd1"
  cmd12="put conf/graph_suning_dsp.conf"
  ftp_cmd $1 "$cmd12"
#  touch data/calibrate.txt.touch
   cmd1="put data/mimn_model/model.pb"
   ftp_cmd $1 "$cmd1"
#  cmd2="put data/calibrate.txt.touch"
#  cmd2="put data/rankscore.txt.touch"
#  ftp_cmd $1 "$cmd2"
}

function put_else_2() {
ftp -n<<!
open $1
user predict predict123
binary
prompt
lcd `pwd`

cd predict
cd predictor/
mput data/mimn_model/*

!

#cd predict
#cd predictor/data
#mkdir mimn_model
#cd ../
}

function online() {
  echo "upload whole file to online $1"

  # copy函数把 /data/niucl/dsp_predictor/ 相应文件拷贝到release下，谨慎执行！！！！
  # 把准备好的文件拷贝到release相应目录下，然后执行上传

   cmd11="put data/ocpx.txt"
#  cmd11="put data/calibrate.txt"
#  cmd12="put conf/graph_suning_dsp.conf"
#  cmd14="put data/redis_user_schema.txt"
#  cmd15="put data/suning_features_ctr_bj.conf"
#  cmd16="put data/suning_features_cvr_bj.conf"
#  cmd17="put data/suning_features_cvr_nj.conf"
#  cmd18="put data/redis_user_schema_bj.txt"
#  cmd19="put lib/libtensorflow_cc.so"
#  cmd20="put lib/libtensorflow_framework.so"
#   cmd21="put data/suning_features_business.conf"
   ftp_cmd $1 "$cmd11"
#  ftp_cmd $1 "$cmd12"
#  ftp_cmd $1 "$cmd13"
#  ftp_cmd $1 "$cmd14"
#  ftp_cmd $1 "$cmd15"
#  ftp_cmd $1 "$cmd16"
#  ftp_cmd $1 "$cmd17"  
#  ftp_cmd $1 "$cmd19"
#  ftp_cmd $1 "$cmd20"
#  ftp_cmd $1 "$cmd21"
#  touch data/suning_features_cvr.conf.touch
#  touch conf/graph_suning_dsp.conf.touch
   sudo touch data/ocpx.txt.touch
#  touch data/rankscore.txt.touch
#  touch data/calibrate.txt.touch
   cmd21="put data/ocpx.txt.touch"
#  cmd22="put data/calibrate.txt.touch"
#  cmd22="put conf/graph_suning_dsp.conf.touch"
#  cmd16="put data/suning_features_cvr.conf.touch"
#  ftp_cmd $1 "$cmd20"
   ftp_cmd $1 "$cmd21"
#   ftp_cmd $1 "$cmd14"
#   ftp_cmd $1 "$cmd15"
#  ftp_cmd $1 "$cmd16"
#  ftp_cmd $1 "$cmd22"
}

function update_model() {
  echo "update_model"
#  cmd1="put data/fm_ctr_bj.model"
#  cmd2="put data/fm_cvr_bj.model"
#  cmd3="put data/fm_cvr_nj.model"
#  cmd4="mput data/mimn_model/*"
   cmd5="put data/xgb_ctr_001.model"

#  ftp_cmd $1 "$cmd1"
#  ftp_cmd $1 "$cmd2"
#  ftp_cmd $1 "$cmd3"
#  ftp_cmd $1 "$cmd4"
   ftp_cmd $1 "$cmd5"
#  touch data/fm_cvr_bj.model.touch
#  touch data/fm_ctr_bj.model.touch
#  touch data/fm_cvr_nj.model.touch

   sudo touch data/xgb_ctr_001.model.touch
   cmd4="put data/xgb_ctr_001.model.touch"
#  cmd1="put data/fm_ctr_bj.model.touch"
#  cmd2="put data/fm_cvr_bj.model.touch"
#  cmd3="put data/fm_cvr_nj.model.touch"

#  ftp_cmd $1 "$cmd1"
#  ftp_cmd $1 "$cmd2"
#  ftp_cmd $1 "$cmd3"
   ftp_cmd $1 "$cmd4"
}

function update_list_conf() {
  echo "upload suning_features_list.conf online $1"

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

#touch data/suning_features_list.conf.touch
#touch data/suning_features_list_cvr.conf.touch

#  ftp -n<<!
#open $1
#user predict predict123
#cd /predictor/
#lcd `pwd`
#binary
#prompt
#put data/suning_features_list_cvr.conf.touch
#close
#bye
#!

}


function list() {
  cd tmp/
  cmd="get data/ocpx.txt $1.txt"
  ftp_cmd $1 "$cmd"
  cd ../
}

function batch_task() {
task_id=$1
file1=$2
ips=$3
echo "ftp config file: "$file1
hosts_line=`sed -n "/$ips/p" $file1`
hosts_str=`echo $hosts_line | sed 's/'$ips'=\([0-9\.,]*\)/\1/g'`
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
if [ $task_id -eq 4 ];then
echo "online: $s..."
online $s
elif [ $task_id -eq 6 ];then
echo "list: $s..."
list $s
elif [ $task_id -eq 8 ];then
echo "update_model: $s..."
update_model $s
elif [ $task_id -eq 9 ];then
put_so $s
elif [ $task_id -eq 10 ];then
update_so $s
elif [ $task_id -eq 11 ];then
update_list_conf $s
elif [ $task_id -eq 99 ];then
put_else $s
else
echo "do nothing"
fi
done
}

if [ $# -eq 0 ];then
echo "args: 
1->copy, 2->upload, 3->online(with 2nd arg ftp ip), 
4->batch online(with 2nd arg ftp ips config file, 3rd arg ftp ips key name), 
5->list(with 2nd arg ftp ip) 
6->batch list(with 2nd arg ftp ips config file, , 3rd arg ftp ips key name)
7->update model(with 2nd arg ftp ip)
8->batch update model(with 2nd arg ftp ips config file, , 3rd arg ftp ips key name)"
elif [ $1 -eq 1 ];then
echo "do copy operation..."
copy
elif [ $1 -eq 2 ];then
echo "do upload operation..."
upload
elif [ $1 -eq 3 ];then
echo "do online operation..." 
online $2
elif [ $1 -eq 4 ];then
echo "do batch online operation..."
#batch_online $2
batch_task $1 $2 $3
elif [ $1 -eq 5 ];then
echo "do list operation..."
list $2
elif [ $1 -eq 6 ];then
echo "do batch list operation..."
#batch_list $2
batch_task $1 $2 $3
elif [ $1 -eq 7 ];then
echo "do update model operation..."
update_model $2
elif [ $1 -eq 8 ];then
echo "do batch update model operation..."
batch_task $1 $2 $3
elif [ $1 -eq 9 ];then
echo "do batch put so operation..."
batch_task $1 $2 $3
elif [ $1 -eq 10 ];then
echo "do batch update so operation..."
batch_task $1 $2 $3
elif [ $1 -eq 11 ];then
echo "do batch update list_conf operation..."
batch_task $1 $2 $3
elif [ $1 -eq 99 ];then
echo "do batch something else operation..."
batch_task $1 $2 $3
else
echo "Illegal args, args: 1->copy, 2->upload, 3->online(with 2nd arg ftp ip), 4->batch online(with 2nd arg ftp ips config file), 5->list(with 2nd arg ftp ip) 6->batch list(with 2nd arg ftp ips config file)"
fi

#copy
#upload
#batch_online $1
#online 10.247.165.10
#online 10.247.165.9
#list 10.247.165.10

