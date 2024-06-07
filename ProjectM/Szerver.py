import socket
import threading

MAX_CONNECTIONS = 5
PORT = 12345


def handle_client(client_socket, positive_count, negative_count):
    # Itt kezeld a klienssel való kommunikációt
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # Kommunikáció feldolgozása
        message = data.decode().lower()
        if message == "igen":
            positive_count += 1
        elif message == "nem":
            negative_count += 1
        client_socket.sendall(data)

    print(f"Positives: {positive_count}, Negatives: {negative_count}")
    client_socket.close()


def main():
    # Socket létrehozása
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f"Listening on port {PORT}...")

    # Fogadás a kliensekkel
    positive_count = 0
    negative_count = 0
    while True:
        try:
            # Korlátozott számú accept
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            # Kliens kezelése új threadben
            client_thread = threading.Thread(target=handle_client, args=(client_socket, positive_count, negative_count))
            client_thread.start()

            # Felszabadulásig való várakozás, ha nincs elég erőforrás
            active_threads = threading.active_count()
            if active_threads >= (MAX_CONNECTIONS + 1):  # Az aktív szálak között a main is benne van, ezért +1
                print("Maximum connections reached. Waiting for resources to be freed...")
                client_thread.join()

        except KeyboardInterrupt:
            print("\nServer stopped.")
            break

    server_socket.close()


if __name__ == "__main__":
    main()