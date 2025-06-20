import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import socket
import threading
import json
from datetime import datetime

class ChatServer:
    def __init__(self):
        self.clients = {}  # {socket: {'username': str, 'address': tuple}}
        self.server_socket = None
        self.is_running = False

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("TCP Chat Server")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")

        self.setup_gui()

        def setup_gui(self):
        # Title
        title_label = tk.Label(self.root, text="TCP Chat Server",
                               font=("Arial", 18, "bold"),
                               bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        # Server controls frame
        control_frame = tk.Frame(self.root, bg="#2c3e50")
        control_frame.pack(pady=10)

        # Host and Port inputs
        tk.Label(control_frame, text="Host:", bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5)
        self.host_entry = tk.Entry(control_frame, width=15)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5)

        # Start/Stop buttons
        self.start_btn = tk.Button(control_frame, text="Start Server",
                                   command=self.start_server, bg="#27ae60", fg="white",
                                   font=("Arial", 10, "bold"))
        self.start_btn.grid(row=0, column=4, padx=10)

        self.stop_btn = tk.Button(control_frame, text="Stop Server",
                                  command=self.stop_server, bg="#e74c3c", fg="white",
                                  font=("Arial", 10, "bold"), state="disabled")
        self.stop_btn.grid(row=0, column=5, padx=5)

        # Status label
        self.status_label = tk.Label(self.root, text="Server Status: Stopped",
                                     bg="#2c3e50", fg="#e74c3c", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Main content frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Connected clients section
        clients_frame = tk.LabelFrame(main_frame, text="Connected Clients",
                                      bg="#34495e", fg="white", font=("Arial", 10, "bold"))
        clients_frame.pack(fill="x", pady=(0, 10))

        self.clients_listbox = tk.Listbox(clients_frame, height=4, bg="#ecf0f1",
                                          font=("Arial", 9))
        self.clients_listbox.pack(fill="x", padx=5, pady=5)

        # Chat messages section
        messages_frame = tk.LabelFrame(main_frame, text="Chat Messages",
                                       bg="#34495e", fg="white", font=("Arial", 10, "bold"))
        messages_frame.pack(fill="both", expand=True)

        self.messages_text = scrolledtext.ScrolledText(messages_frame, height=15,
                                                       bg="#ecf0f1", font=("Arial", 9),
                                                       state="disabled")
        self.messages_text.pack(fill="both", expand=True, padx=5, pady=5)


        tk.Label(control_frame, text="Port:", bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5)
        self.port_entry = tk.Entry(control_frame, width=10)
        self.port_entry.insert(0, "12345")
        self.port_entry.grid(row=0, column=3, padx=5)

        # Server message input
        input_frame = tk.Frame(self.root, bg="#2c3e50")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(input_frame, text="Server Message:", bg="#2c3e50", fg="white").pack(side="left")
        self.server_msg_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.server_msg_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.server_msg_entry.bind("<Return>", self.send_server_message)

        send_btn = tk.Button(input_frame, text="Send", command=self.send_server_message,
                             bg="#3498db", fg="white", font=("Arial", 10, "bold"))
        send_btn.pack(side="right")

    def start_server(self):
        try:
            host = self.host_entry.get() or "localhost"
            port = int(self.port_entry.get())

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)

            self.is_running = True
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.status_label.config(text=f"Server Status: Running on {host}:{port}", fg="#27ae60")

            self.log_message(f"Server started on {host}:{port}")

            # Start accepting clients in a separate thread
            threading.Thread(target=self.accept_clients, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")

    def stop_server(self):
        self.is_running = False

        # Close all client connections
        for client_socket in list(self.clients.keys()):
            try:
                client_socket.close()
            except:
                pass
        self.clients.clear()

       # Close server socket
        if self.server_socket:
            self.server_socket.close()

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Server Status: Stopped", fg="#e74c3c")
        self.update_clients_display()
        self.log_message("Server stopped")

    def accept_clients(self):
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                threading.Thread(target=self.handle_client,
                                 args=(client_socket, address), daemon=True).start()
            except:
                if self.is_running:
                    self.log_message("Error accepting client connections")
                break

    def handle_client(self, client_socket, address):
        try:
            # Wait for username
            data = client_socket.recv(1024).decode('utf-8')
            message = json.loads(data)

            if message['type'] == 'join':
                username = message['username']
                self.clients[client_socket] = {'username': username, 'address': address}

                self.log_message(f"{username} joined from {address}")
                self.update_clients_display()

                # Notify all clients about new user
                self.broadcast_message({
                    'type': 'system',
                    'message': f"{username} joined the chat",
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }, exclude=client_socket)

                # Handle client messages
                while self.is_running:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break

                    message = json.loads(data)
                    if message['type'] == 'message':
                        self.log_message(f"{username}: {message['content']}")
                        self.broadcast_message({
                            'type': 'message',
                            'username': username,
                            'content': message['content'],
                            'timestamp': datetime.now().strftime("%H:%M:%S")
                        })

        except Exception as e:
            pass
        finally:
            self.disconnect_client(client_socket)

    def disconnect_client(self, client_socket):
        if client_socket in self.clients:
            username = self.clients[client_socket]['username']
            del self.clients[client_socket]

            self.log_message(f"{username} disconnected")
            self.update_clients_display()

             # Notify remaining clients
            self.broadcast_message({
                'type': 'system',
                'message': f"{username} left the chat",
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })

        try:
            client_socket.close()
        except:
            pass

    def broadcast_message(self, message, exclude=None):
        message_data = json.dumps(message).encode('utf-8')

        for client_socket in list(self.clients.keys()):
            if client_socket != exclude:
                try:
                    client_socket.send(message_data)
                except:
                    self.disconnect_client(client_socket)

    def send_server_message(self, event=None):
        message = self.server_msg_entry.get().strip()
        if message:
            self.log_message(f"[SERVER]: {message}")
            self.broadcast_message({
                'type': 'server',
                'message': message,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            self.server_msg_entry.delete(0, 'end')

    def update_clients_display(self):
        self.clients_listbox.delete(0, 'end')
        for client_info in self.clients.values():
            self.clients_listbox.insert('end',
                                        f"{client_info['username']} - {client_info['address'][0]}:{client_info['address'][1]}")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.messages_text.config(state="normal")
        self.messages_text.insert('end', f"[{timestamp}] {message}\n")
        self.messages_text.config(state="disabled")
        self.messages_text.see('end')

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if self.is_running:
            self.stop_server()
        self.root.destroy()


if __name__ == "__main__":
    server = ChatServer()
    server.run()



       



