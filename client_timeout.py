import socket

SERVER_IP = "127.0.0.1"
PORT = 5050

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ============================
    # 1. Timeout saat connect
    # ============================
    client.settimeout(3)   # timeout 3 detik

    try:
        client.connect((SERVER_IP, PORT))
        print("Berhasil terhubung ke server.")
    except socket.timeout:
        print("Koneksi timeout!")
        return
    except Exception as e:
        print(f"Error lain: {e}")
        return

    # ============================
    # 2. Timeout saat menerima data
    # ============================
    client.settimeout(2)   # timeout 2 detik untuk recv

    try:
        print("Menunggu data dari server...")
        data = client.recv(1024)
        print("Data diterima:", data.decode())
    except socket.timeout:
        print("Koneksi timeout!")
    except Exception as e:
        print(f"Error lain: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()