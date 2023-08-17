if [ $# -eq 0 ]; then
  echo "Не указаны имена файлов"
  exit 1
fi

for filename in "$@"; do
  if [ ! -f "$filename" ]; then
    echo "Файл $filename не найден"
    continue
  fi

  echo "Время создания файла $filename: $(stat -c %w "$filename")"
  echo "Время последнего изменения файла $filename: $(stat -c %y "$filename")"
  echo "Время последнего доступа к файлу $filename: $(stat -c %x "$filename")"
  echo "----------------------------------------------------"
done

#2 ВЕРСИЯ
echo "--------------------------gawk--------------------------"

if [ $# -eq 0 ]; then
  echo "Не указаны имена файлов"
  exit 1
fi

for filename in "$@"; do
  if [ ! -f "$filename" ]; then
    echo "Файл $filename не найден"
    continue
  fi

  stat -c '%n' $filename
  echo $(stat -c '%y' $filename) $(stat -c '%w' $filename) $(stat -c '%x' $filename) | gawk '{print "Время создания файла:",$4,$5,$6,"\n","Время последнего изменения файла:",$1,$2,$3,"\n","Время последнего доступа к файлу:",$7,$8,$9}'
  echo "----------------------------------------------------"
done
