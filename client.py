import socket

SERVER_IP = '127.0.0.1'   # jika server berjalan di PC yang sama
PORT = 5050

# Membuat socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# Kirim pesan ke server
pesan = "Tes Koneksi"
client_socket.sendall(pesan.encode())

# Terima balasan
data = client_socket.recv(1024)

print("Balasan dari server :", data.decode())

client_socket.close()