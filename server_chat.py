import socket
import threading

HOST = '0.0.0.0'
PORT = 5050

# List untuk menyimpan client yang terhubung
clients = []
client_names = {}

# Lock untuk mengamankan akses ke list clients (karena multi-thread)
clients_lock = threading.Lock()

def broadcast(message, sender_conn=None):
    """
    Mengirim pesan ke semua client lain (broadcast).
    sender_conn: socket client pengirim (tidak ikut dikirimi pesan).
    """
    with clients_lock:
        for client in clients:
            if client != sender_conn:
                try:
                    client.sendall(message)
                except:
                    # Kalau gagal kirim, kita bisa abaikan atau remove client-nya
                    pass

def handle_client(conn, addr):
    print(f"[TERHUBUNG] {addr}")

    try:
        # Minta nama client
        conn.sendall(b"Masukkan nama Anda: ")
        name_data = conn.recv(1024)
        if not name_data:
            conn.close()
            return

        name = name_data.decode().strip()
        client_names[conn] = name

        # Umumkan bahwa client baru bergabung
        join_msg = f"[SERVER] {name} telah bergabung ke chat.\n".encode()
        print(join_msg.decode().strip())
        broadcast(join_msg, sender_conn=None)

        # Loop utama: terima pesan dari client
        while True:
            data = conn.recv(1024)
            if not data:
                break

            text = data.decode().strip()
            if text == "":
                continue

            # Format pesan: [nama] isi_pesan
            full_msg = f"[{name}] {text}\n"
            print(full_msg.strip())

            # Broadcast ke client lain
            broadcast(full_msg.encode(), sender_conn=conn)

    except Exception as e:
        print(f"[ERROR] Client {addr} error: {e}")

    finally:
        # Jika client disconnect
        with clients_lock:
            if conn in clients:
                clients.remove(conn)

        leave_msg = f"[SERVER] {client_names.get(conn, 'Seorang user')} telah keluar.\n".encode()
        print(leave_msg.decode().strip())
        broadcast(leave_msg, sender_conn=None)

        client_names.pop(conn, None)
        conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[START] Server chat berjalan di port {PORT}")
    print("[INFO] Menunggu client terhubung...")

    try:
        while True:
            conn, addr = server_socket.accept()
            with clients_lock:
                clients.append(conn)

            # Buat thread baru untuk handle client ini
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server dimatikan.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()