import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import socket
import threading
import json
from datetime import datetime


class ChatClient:
    def __init__(self):
        self.client_socket = None
        self.connected = False
        self.username = ""

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("TCP Chat Client")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        self.setup_gui()

   def setup_gui(self):
        # Title
        title_label = tk.Label(self.root, text="TCP Chat Client",
                               font=("Arial", 18, "bold"),
                               bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        # Connection frame
        conn_frame = tk.Frame(self.root, bg="#2c3e50")
        conn_frame.pack(pady=10)

        # Server connection inputs
        tk.Label(conn_frame, text="Server:", bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5)
        self.host_entry = tk.Entry(conn_frame, width=15)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5)

        tk.Label(conn_frame, text="Port:", bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5)
        self.port_entry = tk.Entry(conn_frame, width=10)
        self.port_entry.insert(0, "12345")
        self.port_entry.grid(row=0, column=3, padx=5)

        tk.Label(conn_frame, text="Username:", bg="#2c3e50", fg="white").grid(row=0, column=4, padx=5)
        self.username_entry = tk.Entry(conn_frame, width=15)
        self.username_entry.grid(row=0, column=5, padx=5)

        # Connect/Disconnect buttons
        self.connect_btn = tk.Button(conn_frame, text="Connect",
                                     command=self.connect_to_server, bg="#27ae60", fg="white",
                                     font=("Arial", 10, "bold"))
        self.connect_btn.grid(row=0, column=6, padx=10)

        self.disconnect_btn = tk.Button(conn_frame, text="Disconnect",
                                        command=self.disconnect_from_server, bg="#e74c3c", fg="white",
                                        font=("Arial", 10, "bold"), state="disabled")
        self.disconnect_btn.grid(row=0, column=7, padx=5)

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Disconnected",
                                     bg="#2c3e50", fg="#e74c3c", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Chat display frame
        chat_frame = tk.LabelFrame(self.root, text="Chat Messages",
                                   bg="#34495e", fg="white", font=("Arial", 12, "bold"))
        chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Chat messages display
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=15,
                                                      bg="#ecf0f1", font=("Arial", 10),
                                                      state="disabled", wrap="word")
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure text tags for different message types
        self.chat_display.tag_configure("system", foreground="#7f8c8d", font=("Arial", 10, "italic"))
        self.chat_display.tag_configure("server", foreground="#e74c3c", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("own", foreground="#2980b9", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("other", foreground="#27ae60", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("private_sent", foreground="#8e44ad", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("private_received", foreground="#d35400", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("timestamp", foreground="#95a5a6", font=("Arial", 8))

       # Message type selection frame
        msg_type_frame = tk.LabelFrame(self.root, text="Message Type",
                                       bg="#34495e", fg="white", font=("Arial", 11, "bold"))
        msg_type_frame.pack(fill="x", padx=10, pady=(0, 5))

        type_selection_frame = tk.Frame(msg_type_frame, bg="#34495e")
        type_selection_frame.pack(fill="x", padx=10, pady=5)

        self.message_type = tk.StringVar(value="public")

        public_radio = tk.Radiobutton(type_selection_frame, text="📢 Public (All Users)",
                                      variable=self.message_type, value="public",
                                      bg="#34495e", fg="white", selectcolor="#2c3e50",
                                      font=("Arial", 10), command=self.on_message_type_change)
        public_radio.pack(side="left", padx=(0, 20))

        private_radio = tk.Radiobutton(type_selection_frame, text="🔒 Private Message",
                                       variable=self.message_type, value="private",
                                       bg="#34495e", fg="white", selectcolor="#2c3e50",
                                       font=("Arial", 10), command=self.on_message_type_change)
        private_radio.pack(side="left")

        # Private message target frame (initially hidden)
        self.private_frame = tk.Frame(msg_type_frame, bg="#34495e")

        tk.Label(self.private_frame, text="To:", bg="#34495e", fg="white",
                 font=("Arial", 10)).pack(side="left", padx=(10, 5))

        self.target_entry = tk.Entry(self.private_frame, width=20, font=("Arial", 10))
        self.target_entry.pack(side="left", padx=(0, 10))

        tk.Label(self.private_frame, text="💡 Enter the username of the recipient",
                 bg="#34495e", fg="#bdc3c7", font=("Arial", 9, "italic")).pack(side="left")

       # Message input frame
        input_frame = tk.LabelFrame(self.root, text="Send Message",
                                    bg="#34495e", fg="white", font=("Arial", 12, "bold"))
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Message input area
        msg_input_frame = tk.Frame(input_frame, bg="#34495e")
        msg_input_frame.pack(fill="x", padx=10, pady=10)

        self.message_status_label = tk.Label(msg_input_frame, text="💬 Type your public message:",
                                             bg="#34495e", fg="white", font=("Arial", 10))
        self.message_status_label.pack(anchor="w")

        # Message input
        self.message_entry = tk.Entry(msg_input_frame, font=("Arial", 12),
                                      state="disabled", bg="#ecf0f1",
                                      relief="solid", bd=2)
        self.message_entry.pack(fill="x", pady=(5, 5))
        self.message_entry.bind("<Return>", self.send_message)

        # Instructions
        self.instruction_label = tk.Label(msg_input_frame,
                                          text="💡 Press Enter to send message or click the button below",
                                          bg="#34495e", fg="#bdc3c7", font=("Arial", 9, "italic"))
        self.instruction_label.pack(anchor="w", pady=(0, 5))

        # Send button
        self.send_btn = tk.Button(msg_input_frame, text="📤 SEND MESSAGE",
                                  command=self.send_message,
                                  bg="#27ae60", fg="white",
                                  font=("Arial", 12, "bold"),
                                  state="disabled", height=2)
        self.send_btn.pack(fill="x")

        # Welcome message
        self.display_message("Welcome to TCP Chat Client!", "system")
        self.display_message("Enter server details and username, then click Connect.", "system")
        self.display_message("You can send public messages to all users or private messages to specific users.",
                             "system")
        self.display_message("For private messages, select 'Private Message' and enter the recipient's username.",
                             "system")

    def on_message_type_change(self):
        """Handle message type change between public and private"""
        if self.message_type.get() == "public":
            self.message_status_label.config(text="💬 Type your public message:")
            self.send_btn.config(text="📤 SEND TO ALL", bg="#27ae60")
            self.instruction_label.config(text="💡 Message will be sent to all connected users")
            self.private_frame.pack_forget()
        else:
            self.message_status_label.config(text="🔒 Type your private message:")
            self.send_btn.config(text="📤 SEND PRIVATE", bg="#8e44ad")
            self.instruction_label.config(text="💡 Message will be sent privately to the specified user")
            self.private_frame.pack(fill="x", pady=(5, 0))

    def connect_to_server(self):
        try:
            host = self.host_entry.get().strip() or "localhost"
            port = int(self.port_entry.get().strip() or "12345")
            username = self.username_entry.get().strip()

            if not username:
                messagebox.showerror("Error", "Please enter a username")
                return

            # Create socket and connect
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))

            # Send join message
            join_message = json.dumps({
                'type': 'join',
                'username': username
            })
            self.client_socket.send(join_message.encode('utf-8'))

            self.connected = True
            self.username = username

            # Update GUI
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            self.message_entry.config(state="normal")
            self.send_btn.config(state="normal")
            self.target_entry.config(state="normal")
            self.status_label.config(text=f"Status: Connected as {username}", fg="#27ae60")

            # Disable connection inputs
            self.host_entry.config(state="disabled")
            self.port_entry.config(state="disabled")
            self.username_entry.config(state="disabled")

            self.display_message(f"Connected to server at {host}:{port}", "system")

            # Start listening for messages
            threading.Thread(target=self.listen_for_messages, daemon=True).start()

        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Could not connect to server. Make sure the server is running.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid port number")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def disconnect_from_server(self):
        self.connected = False

        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

        # Update GUI
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")
        self.message_entry.config(state="disabled")
        self.send_btn.config(state="disabled")
        self.target_entry.config(state="disabled")
        self.status_label.config(text="Status: Disconnected", fg="#e74c3c")

        # Enable connection inputs
        self.host_entry.config(state="normal")
        self.port_entry.config(state="normal")
        self.username_entry.config(state="normal")

        self.display_message("Disconnected from server", "system")

    def listen_for_messages(self):
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Debug: Print what we received
                print(f"Received: {data}")

                message = json.loads(data)

                if message['type'] == 'message':
                    # Public message from another user
                    if message['username'] != self.username:
                        self.display_message(
                            f"{message['username']}: {message['content']}",
                            "other",
                            message['timestamp']
                        )

                elif message['type'] == 'private_message':
                    # Private message received
                    self.display_message(
                        f"🔒 Private from {message['sender']}: {message['content']}",
                        "private_received",
                        message['timestamp']
                    )

                elif message['type'] == 'private_confirmation':
                    # Confirmation that private message was sent
                    if message.get('delivered', False):
                        self.display_message(
                            f"🔒 Private to {message['target']}: {message['content']}",
                            "private_sent",
                            message['timestamp']
                        )
                    else:
                        self.display_message(
                            f"❌ Failed to deliver private message to {message['target']}: {message.get('reason', 'User not found')}",
                            "system",
                            message['timestamp']
                        )

                elif message['type'] == 'error':
                    # Server error message
                    self.display_message(f"❌ Server Error: {message.get('message', 'Unknown error')}", "system")

                elif message['type'] == 'system':
                    self.display_message(message['message'], "system", message['timestamp'])

                elif message['type'] == 'server':
                    self.display_message(f"[SERVER]: {message['message']}", "server", message['timestamp'])

                else:
                    # Unknown message type - for debugging
                    print(f"Unknown message type: {message}")
                    self.display_message(f"Unknown message type: {message['type']}", "system")

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                self.display_message("Received invalid message format", "system")
            except Exception as e:
                print(f"Listen error: {e}")
                if self.connected:
                    self.display_message("Connection lost", "system")
                    self.disconnect_from_server()
                break

    def send_message(self, event=None):
        """Send message based on selected type (public or private)"""
        if not self.connected:
            messagebox.showwarning("Not Connected", "Please connect to server first!")
            return

        message = self.message_entry.get().strip()
        if not message:
            return

        try:
            if self.message_type.get() == "public":
                # Send public message
                message_data = json.dumps({
                    'type': 'message',
                    'content': message
                })
                self.client_socket.send(message_data.encode('utf-8'))

                # Display own public message
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.display_message(f"You: {message}", "own", timestamp)

            else:  # private message
                target_user = self.target_entry.get().strip()
                if not target_user:
                    messagebox.showwarning("Missing Recipient", "Please enter the username of the recipient!")
                    self.target_entry.focus()
                    return

                if target_user == self.username:
                    messagebox.showwarning("Invalid Target", "You cannot send a private message to yourself!")
                    return

                # Send private message
                message_data = json.dumps({
                    'type': 'private_message',
                    'target': target_user,
                    'content': message
                })

                # Debug: Show what we're sending
                print(f"Sending private message: {message_data}")
                self.display_message(f"🔄 Sending private message to {target_user}...", "system")

                self.client_socket.send(message_data.encode('utf-8'))

               # Note: We'll get a confirmation from server if message is delivered

            self.message_entry.delete(0, 'end')
            self.message_entry.focus()

        except Exception as e:
            self.display_message(f"Failed to send message: {str(e)}", "system")
            messagebox.showerror("Send Error", f"Could not send message: {e}")
            print(f"Send error: {e}")

    def display_message(self, message, msg_type="normal", timestamp=None):
        self.chat_display.config(state="normal")

        if timestamp:
            self.chat_display.insert('end', f"[{timestamp}] ", "timestamp")

        self.chat_display.insert('end', f"{message}\n", msg_type)
        self.chat_display.config(state="disabled")
        self.chat_display.see('end')

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if self.connected:
            self.disconnect_from_server()
        self.root.destroy()


       



       
       

