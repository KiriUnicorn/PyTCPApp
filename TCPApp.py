import os
import tkinter as tk
import time
from tkinter import scrolledtext, messagebox
import socket
import threading


class TCPChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("基于TCP的信息发送")

        # 目的IP地址输入框
        self.label_ip = tk.Label(master, text="目的IP地址:")
        self.label_ip.pack()
        self.entry_ip = tk.Entry(master, relief=tk.SOLID, bd=1)
        self.entry_ip.pack()

        # 目的端口输入框
        self.label_port = tk.Label(master, text="目的端口:")
        self.label_port.pack()
        self.entry_port = tk.Entry(master, relief=tk.SOLID, bd=1)
        self.entry_port.pack()

        # 发送的消息框
        self.label_message = tk.Label(master, text="发送的消息:")
        self.label_message.pack()
        self.entry_message = tk.Entry(master, width=80, relief=tk.SOLID, bd=1)
        self.entry_message.pack()

        # 接收消息显示框
        self.label_received = tk.Label(master, text="接收的消息:")
        self.label_received.pack()

        self.text_received = scrolledtext.ScrolledText(master, width=80, height=20, relief=tk.SOLID, bd=1)
        self.text_received.pack()
        self.text_received.tag_configure('right_aligned', justify='right')

        # 发送按钮
        self.send_button = tk.Button(master, text="发送", command=self.send_message, relief=tk.SOLID, bd=2)
        self.send_button.pack()

        # 创建服务器线程
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def send_message(self):
        # 获取输入的目的IP、目的端口和消息

        target_ip = self.entry_ip.get()
        target_port = int(self.entry_port.get())
        message = self.entry_message.get()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))
        client.send(message.encode())
        client.close()

        # 在接收消息框中显示发送的消息

        send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.text_received.insert(tk.END, f"{send_time}【发送到】--->{target_ip}:{target_port}的消息: \n{message}\n\n")
        # 清空消息输入框
        self.entry_message.delete(0, tk.END)

    # 添加了一个start_server方法来启动一个简单的TCP服务器，
    # 它会在本地地址的9999端口监听连接。当有新的连接时，
    # 会为每个客户端创建一个新的线程（handle_client方法）来处理消息。
    def start_server(self):
        # 创建TCP服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 9999))
        server_socket.listen(5)

        while True:
            # 等待客户端连接
            client_socket, client_address = server_socket.accept()

            # 创建新的线程来处理客户端消息
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            # 接收客户端消息
            data = client_socket.recv(1024)
            if not data:
                break
            get_recv_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            ip_add_port = client_socket.getpeername()
            ip_add, port = ip_add_port
            # 在接收消息框中显示接收到的消息
            self.text_received.insert(tk.END,
                                      f"{get_recv_time}【来自】<---{ip_add}:{port}的消息:\n{data.decode('utf-8')}\n\n")

        # 关闭客户端连接
        client_socket.close()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            os.abort()
        else:
            pass


def main():
    root = tk.Tk()
    app = TCPChatGUI(root)
    root.mainloop()
    root.protocol("WM_DELETE_WINDOW", app.on_closing())


if __name__ == "__main__":
    main()
