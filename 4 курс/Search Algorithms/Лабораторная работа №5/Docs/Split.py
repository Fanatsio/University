def split_text_into_files(input_filename, num_parts=10):
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_filename}' не найден.")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    words = text.split()
    total_words = len(words)
    
    if total_words == 0:
        print("Ошибка: Файл пустой.")
        return
        
    words_per_part = total_words // num_parts

    for part_num in range(num_parts):
        start = part_num * words_per_part
        end = total_words if part_num == num_parts - 1 else (part_num + 1) * words_per_part

        part_words = words[start:end]
        part_text = ' '.join(part_words)

        output_filename = f'часть_{part_num + 1}.txt'
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(part_text)
            print(f"Создан файл: {output_filename}")
        except Exception as e:
            print(f"Ошибка при записи файла {output_filename}: {e}")

    print(f"Разделение завершено! Создано {num_parts} файлов.")

if __name__ == "__main__":
    INPUT_FILE = 'Властелин_колец_Братство_кольца.txt'
    split_text_into_files(INPUT_FILE)
