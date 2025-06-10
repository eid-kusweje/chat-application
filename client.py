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

       
       

