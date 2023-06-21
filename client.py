import tkinter as tk
from tkinter import messagebox
import Pyro4

@Pyro4.expose
class FileClient:
    def __init__(self):
        self.server = None

    def connect_to_server(self):
        try:
            ns = Pyro4.locateNS()
            uri = ns.lookup("fileserver")
            self.server = Pyro4.Proxy(uri)
            messagebox.showinfo("Connection", "Connected to server successfully!")
        except Pyro4.errors.NamingError:
            messagebox.showerror("Connection", "Failed to connect to the server.")

    def register_interest(self):
        filename = self.filename_entry.get()
        valid_time = int(self.valid_time_entry.get())

        if not self.server:
            messagebox.showerror("Error", "Not connected to the server.")
            return

        self.server.register_interest(self, filename, valid_time)
        messagebox.showinfo("Interest", f"Registered interest for file '{filename}'.")

    def notify_event(self, filename, content):
        messagebox.showinfo("Notification", f"Received notification for file '{filename}':\n{content}")

def main():
    client = FileClient()

    root = tk.Tk()
    root.title("File Client")

    connect_button = tk.Button(root, text="Connect to Server", command=client.connect_to_server)
    connect_button.pack()

    filename_label = tk.Label(root, text="File Name:")
    filename_label.pack()
    client.filename_entry = tk.Entry(root)
    client.filename_entry.pack()

    valid_time_label = tk.Label(root, text="Valid Time (seconds):")
    valid_time_label.pack()
    client.valid_time_entry = tk.Entry(root)
    client.valid_time_entry.pack()

    register_button = tk.Button(root, text="Register Interest", command=client.register_interest)
    register_button.pack()

    root.geometry("400x200")
    root.mainloop()

if __name__ == '__main__':
    main()
