import cv2
import socket
import pickle
import struct

# Настройка сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9999))
server_socket.listen(1)
print("Ожидание подключения...")
conn, addr = server_socket.accept()
print(f"Подключено: {addr}")

# Захват видео
cap = cv2.VideoCapture(0)  # 0 - первая камера

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Сериализация кадра
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))

    # Отправка размера и данных
    conn.sendall(message_size + data)

cap.release()
conn.close()