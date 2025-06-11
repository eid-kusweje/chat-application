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

       


       
       

