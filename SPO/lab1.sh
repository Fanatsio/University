echo "--------------------------Переменные оболочки--------------------------"
for n in $@;
	do
    stat -c '%n' $n
		stat -c '%x' $n
		stat -c '%y' $n
		stat -c '%w' $n
  done
echo "--------------------------gawk--------------------------"
for n in $@;
	do
    stat -c '%n' $n
    echo $(stat -c '%y' $n) $(stat -c '%w' $n) $(stat -c '%x' $n) | gawk '{print "File last modified time:",$1,$2,$3,"\n","File creation time:",$4,$5,$6,"\n","File last access time:",$7,$8,$9}'
  done
echo "--------------------------Командная подстановка--------------------------"
for n in $@;
  do
    script_name=`stat -c '%n' $n`
    script_time=`stat -c '%x' $n; stat -c '%y' $n; stat -c '%w' $n;`
    echo "$script_name 
$script_time"
  done
