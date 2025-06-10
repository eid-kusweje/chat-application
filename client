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
