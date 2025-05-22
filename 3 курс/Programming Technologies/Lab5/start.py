import subprocess

files_to_run = ["adaptive-huffman-compress.py", "adaptive-huffman-decompress.py", "compare_ppm_files.py"]

for file in files_to_run:
    result = subprocess.run(["python", file], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка при выполнении {file}: {result.stderr}")
    else:
        print(f"{file} выполнен успешно: {result.stdout}")
