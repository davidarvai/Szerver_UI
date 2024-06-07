import tkinter as tk
import socket

class ClientUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Client UI")

        self.entry_frame = tk.Frame(root)
        self.entry_frame.grid(row=0, column=0, padx=10, pady=10)

        self.text_entry = tk.Entry(self.entry_frame, width=40)
        self.text_entry.grid(row=0, column=0)

        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=1, column=0, padx=10, pady=5)

        self.send_button = tk.Button(self.button_frame, text="Send", command=self.send_text, bg="#D4EFDF")
        self.send_button.grid(row=0, column=0, padx=(0, 5))

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_client, bg="#FF5733")
        self.exit_button.grid(row=0, column=1, padx=(5, 0))

        self.text_area_received = tk.Text(root, state='disabled', width=40, height=10)
        self.text_area_received.grid(row=2, column=0, padx=10, pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))

    def send_text(self):
        message = self.text_entry.get()
        self.text_area_received.config(state='normal')
        self.text_area_received.insert('end', f"Sent to server: {message}\n")
        self.text_area_received.config(state='disabled')
        self.client_socket.sendall(message.encode())
        self.text_entry.delete(0, 'end')

        if message.lower() == "exit":
            self.exit_client()

    def exit_client(self):
        self.text_area_received.config(state='normal')
        self.text_area_received.insert('end', f"Disconnected from server\n")
        self.text_area_received.config(state='disabled')
        self.client_socket.sendall("exit".encode())
        self.client_socket.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    client_ui = ClientUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()