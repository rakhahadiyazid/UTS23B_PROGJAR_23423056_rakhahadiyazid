import socket
import threading

SERVER_IP = '127.0.0.1'  # ganti ke IP server kalau beda komputer
PORT = 5050

def terima_pesan(sock):
    """
    Thread untuk terus-menerus menerima pesan dari server
    dan menampilkannya ke layar.
    """
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[INFO] Koneksi ke server terputus.")
                break
            print("\n" + data.decode(), end="")  # tampilkan pesan
            print("> ", end="", flush=True)      # prompt lagi
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    # Terima pesan awal dari server (minta nama)
    data = sock.recv(1024)
    print(data.decode(), end="")
    name = input()
    sock.sendall(name.encode())

    # Buat thread untuk menerima pesan dari server
    t = threading.Thread(target=terima_pesan, args=(sock,), daemon=True)
    t.start()

    print("Ketik pesan, atau 'quit' untuk keluar.\n")

    while True:
        try:
            msg = input("> ")
            if msg.lower() == "quit":
                break
            if msg.strip() == "":
                continue
            sock.sendall(msg.encode())
        except KeyboardInterrupt:
            break
        except:
            break

    sock.close()
    print("Keluar dari chat.")

if __name__ == "__main__":
    main()