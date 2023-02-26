echo "--------------------------Переменные оболочки--------------------------"
for n in $@;
	do
    stat -c '%n' $n
		stat -c '%x' $n
		stat -c '%y' $n
		stat -c '%w' $n
  done
echo "--------------------------gawk--------------------------"
echo $(stat -c '%y' $@) $(stat -c '%w' $@) $(stat -c '%x' $@) | gawk '{print "File last modified time:",$1,$2,"\n","File creation time:",$4,$5,"\n","File last access time:",$7,$6}'
echo "--------------------------Командная подстановка--------------------------"
for n in $@;
  do
    script_name=`stat -c '%n' $n`
    script_time=`stat -c '%x' $n; stat -c '%y' $n; stat -c '%w' $n;`
    echo "$script_name 
$script_time"
  done
