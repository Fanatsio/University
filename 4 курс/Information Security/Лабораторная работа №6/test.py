import platform
import psutil
import uuid
import hashlib
import os

def get_hash(message, salt="SecureApp2026"):
    salted_message = (salt + message.decode('utf-8')).encode('utf-8')
    return hashlib.sha256(salted_message).hexdigest()

def get_hardware_info():
    try:
        system_info = platform.system() + platform.node()
        cpu_info = platform.processor()
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)])
        disk_info = ""
        
        for partition in psutil.disk_partitions():
            try:
                disk_info += partition.device + str(psutil.disk_usage(partition.mountpoint).total)
            except (OSError, PermissionError):
                continue

        hardware_id = f"{system_info}{cpu_info}{mac_address}{disk_info}"
        return hardware_id
    except Exception as e:
        print(f"Ошибка при сборе информации об оборудовании: {e}")
        raise

def check_license():
    try:
        current_hardware_info = get_hardware_info()
        current_hash = get_hash(current_hardware_info.encode('utf-8'))
        license_path = os.path.join(os.path.dirname(__file__), 'license.txt')
        
        try:
            with open(license_path, 'r') as file:
                saved_hash = file.read().strip()
        except FileNotFoundError:
            try:
                with open(license_path, 'w') as file:
                    file.write(current_hash)
                print("Программа успешно установлена на этом компьютере.")
                return True
            except IOError as e:
                print(f"Ошибка при записи файла лицензии: {e}")
                return False

        if current_hash == saved_hash:
            print("Программа запущена легально.")
            return True
        else:
            print("Обнаружено нелегальное использование программы!")
            return False
    except Exception as e:
        print(f"Ошибка при проверке лицензии: {e}")
        return False

if __name__ == "__main__":
    if check_license():
        print("Программа продолжает работу...")
    else:
        print("Программа завершает работу.")
        exit(1)