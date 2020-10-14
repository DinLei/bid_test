
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


a=`find data/ -name '*list*.conf'`

echo $a

arr=($a)

for s in ${arr[@]}
do
echo $s
cmd1="put $s"
ftp_cmd '10.96.19.101' $cmd1
done
