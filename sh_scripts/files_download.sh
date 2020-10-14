#/bin/bash

function ftp_cmd() {
ftp -n<<!
open ossftp.suning.com
user aps/dmp_ftp/jrttdmp 432fcfc6d292eecf848f63909dae5127
cd /jrtt/spider/pachong/baidu_18128421/spider/pachong/baidu_18128421
lcd `pwd`
$1
close
bye
!
}

function bisheng_upload() {
  bish_cmd="get online_bisheng.tar"
  ftp_cmd "$bish_cmd"
  
  tar -xf online_bisheng.tar
  
  tmp_path=check/last_online_bisheng
  if [ ! -d "$tmp_path" ]; then  
　　mkdir "$tmp_path"  
  fi 
  cp -rf /opt/predict/predictor/dsp_predictor/deps/include/bisheng check/last_online_bisheng
  cp -f /opt/predict/predictor/dsp_predictor/deps/lib/libbisheng.a check/last_online_bisheng

  cp -rf tmp_online_bisheng/bisheng /opt/predict/predictor/dsp_predictor/deps/include/
  cp -f tmp_online_bisheng/libbisheng.a /opt/predict/predictor/dsp_predictor/deps/lib/

  rm -rf tmp_online_bisheng
  rm -f online_bisheng.tar

}

function model_upload() {
  mo_cmd="get fm.model"
  ftp_cmd "$mo_cmd"

  cp /opt/predict/predictor/dsp_predictor/release/data/fm.model ./fm.model.last
  
  cp -f fm.model /opt/predict/predictor/dsp_predictor/release/data/
  cp -f fm.model /opt/predict/predictor/dsp_predictor/data/

  rm fm.model
}


if [ $# -eq 0 ];then
echo "args:
1 -> upload fm.model
2 -> upload bisheng files"
elif [ $1 -eq 1 ];then
echo "do upload fm.model operation..."
model_upload
elif [ $1 -eq 2 ];then
echo "do upload bisheng files operation..."
bisheng_upload
else
echo "
Illegal args, 
args: 
1 -> upload fm.model, 
2 -> upload bisheng files"
fi

