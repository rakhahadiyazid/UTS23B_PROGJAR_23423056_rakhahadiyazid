import socket

HOST = '0.0.0.0'   # menerima koneksi dari semua alamat
PORT = 5050        # port sesuai soal

# Membuat socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server berjalan di port {PORT}...")
print("Menunggu koneksi client...")

while True:
    conn, addr = server_socket.accept()
    print(f"Terhubung dengan client: {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break

        pesan = data.decode()
        print(f"Dari client: {pesan}")

        # Kirim kembali ke client
        conn.sendall(data)

    conn.close()
    print("Client terputus.\n")