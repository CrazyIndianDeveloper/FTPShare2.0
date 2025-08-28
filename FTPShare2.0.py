# Author: Crazy Indian Developer (Vijay Mahajan)
# Date: 2025-08-28
# Description: Simple GUI FTP server script using pyftpdlib for file sharing in local network
# Version: 2.0


import tkinter as tk
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import threading
import socket
from tkinter import messagebox
import webbrowser
from tkinter import Menu


def update_textarea(message, color):
    def callback():
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, message)
        text_area.config(fg=color)
        text_area.config(state=tk.DISABLED)

    root.after(0, callback)


def start_server():
    # Disable the Start Server button
    start_button.config(state=tk.DISABLED)

    # Enable the Stop Server button
    stop_button.config(state=tk.NORMAL)

    # Update the text area
    update_textarea("Server Started\n", "green")

    # Set up anonymous user
    authorizer = DummyAuthorizer()
    cwd = os.getcwd()
    authorizer.add_anonymous(cwd, perm="elradfmw")

    # Set up FTP handler
    handler = FTPHandler
    handler.authorizer = authorizer

    # Create FTP server
    root.server = FTPServer(("0.0.0.0", 2121), handler)

    # Listening on port 2121

    # Starting server in separate thread
    def run_server():
        root.server.serve_forever()

    root.server_thread = threading.Thread(target=run_server)
    root.server_thread.start()
    root.running = True

    ip_list = []
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            ip_list.append(ip)

    for ip in ip_list:
        # Update the text area
        update_textarea("FTPShare2.0 Server Started on ftp://" + ip + ":2121\n", "green")


def stop_server():
    if root.server:
        # Set running flag to False to stop the server
        root.running = False
        root.server.close_all()

        # root.server_thread.join() # <------ This Line Cause Trouble in Linux | taking too much time to close thread and freeze the application
        # Wait for the thread to finish
        # In Windows it works fine

    stop_button.config(state=tk.DISABLED)
    # Disable the Stop Server button

    start_button.config(state=tk.NORMAL)
    # Enable the Start Server button

    update_textarea("Server Stopped\n", "red")
    # Update the text area


def on_closing():
    if messagebox.askokcancel("FTPShare 2.0", "Do you want to quit?"):
        root.destroy()
        stop_server()


# Main Window
root = tk.Tk()
root.title("FTPShare 2.0")
root.geometry("500x220")

# Menubar
menubar = Menu(root)

# Menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='More Free Tools', menu=file)


def open_youtube():
    webbrowser.open(
        "https://www.youtube.com/channel/UCnij5U2Ic3PtpzCWmmydP7g?sub_confirmation=1")  # Opens YouTube in the default browser


def open_github():
    webbrowser.open("https://github.com/CrazyIndianDeveloper")  # Opens GitHub in the default browser


def open_instagram():
    webbrowser.open("https://www.instagram.com/crazy_indian_developer/")  # Opens Instagram in the default browser


def open_x():
    webbrowser.open("https://x.com/mahajan__vijay")  # Opens Twitter in the default browser


file.add_command(label='YouTube', command=open_youtube)
file.add_command(label='GitHub', command=open_github)
file.add_command(label='Instagram', command=open_instagram)
file.add_command(label='Twitter ( X )', command=open_x)
file.add_separator()
file.add_command(label='Crazy Indian Developer ( Vijay Mahajan )', command=None)

# Buttons and text area
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.pack(pady=10)

text_area = tk.Text(root, height=6, width=55, wrap=tk.WORD, state=tk.DISABLED)
text_area.pack(pady=10)

stop_button = tk.Button(root, text="Stop Server", command=stop_server, state=tk.DISABLED)  # Disabled at beginning
stop_button.pack(pady=10)

icon = tk.PhotoImage(file='ftp.png')
root.iconphoto(True, icon)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.config(menu=menubar)

root.mainloop()
