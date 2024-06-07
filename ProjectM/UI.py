import tkinter as tk
import socket
import threading

MAX_CONNECTIONS = 5
PORT = 12345
SERVER_ADDRESS = ('localhost', PORT)


class ServerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Server UI")

        self.text_area_received = tk.Text(root, state='disabled', width=40, height=10)
        self.text_area_received.grid(row=0, column=0, padx=10, pady=10)

        self.text_area_sent = tk.Text(root, state='disabled', width=40, height=10)
        self.text_area_sent.grid(row=1, column=0, padx=10, pady=10)

        self.start_server_button = tk.Button(root, text="Start Server", command=self.start_server, bg="#28a745")
        self.start_server_button.grid(row=2, column=0, padx=10, pady=5)

        self.stop_server_button = tk.Button(root, text="Stop Server", command=self.stop_server, state='disabled',bg="#45B39D")
        self.stop_server_button.grid(row=3, column=0, padx=10, pady=5)

        self.update_button = tk.Button(root, text="Display Votes", command=self.update_vote_counts)
        self.update_button.grid(row=4, column=0, padx=10, pady=5)

        self.server_socket = None
        self.server_thread = None
        self.positive_count = 0
        self.negative_count = 0
        self.clients = []

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', PORT))
        self.server_socket.listen(MAX_CONNECTIONS)
        self.text_area_received.config(state='normal')
        self.text_area_received.insert('end', f"Listening on port {PORT}...\n")
        self.text_area_received.config(state='disabled')
        self.start_server_button.config(state='disabled')
        self.stop_server_button.config(state='normal')

        self.server_thread = threading.Thread(target=self.accept_clients)
        self.server_thread.start()

    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
        if self.server_thread:
            self.server_thread.join()
        self.print_counts()
        self.start_server_button.config(state='normal')
        self.stop_server_button.config(state='disabled')

    def accept_clients(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                self.clients.append(client_socket)
                self.text_area_received.config(state='normal')
                self.text_area_received.insert('end', f"Accepted connection from {addr}\n")
                self.text_area_received.config(state='disabled')
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
            except Exception as e:
                print("Exception:", e)
                break

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode().lower()
            if message == "igen":
                self.positive_count += 1
            elif message == "nem":
                self.negative_count += 1
            elif message == "exit":
                self.clients.remove(client_socket)
                self.text_area_received.config(state='normal')
                self.text_area_received.insert('end', f"Client disconnected\n")
                self.text_area_received.config(state='disabled')
                break
            self.text_area_received.config(state='normal')
            self.text_area_received.insert('end', f"Received from client: {message}\n")
            self.text_area_received.config(state='disabled')

            response = f"Received from server: {message}"
            self.text_area_sent.config(state='normal')
            self.text_area_sent.insert('end', response + '\n')
            self.text_area_sent.config(state='disabled')

            client_socket.sendall(response.encode())

        client_socket.close()

    def print_counts(self):
        self.text_area_received.config(state='normal')
        self.text_area_received.insert('end',
                                       f"Positive_Vote: {self.positive_count}, Negative_Vote: {self.negative_count}\n")
        self.text_area_received.config(state='disabled')
        self.clients.clear()

    def update_vote_counts(self):
        self.text_area_received.config(state='normal')
        self.text_area_received.insert('end',
                                       f"Positive_Vote: {self.positive_count}, Negative_Vote: {self.negative_count}\n")
        self.text_area_received.config(state='disabled')


def main():
    root = tk.Tk()
    server_ui = ServerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()