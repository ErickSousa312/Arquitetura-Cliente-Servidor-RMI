# saved as greeting-client.py
import Pyro4
import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import base64

@Pyro4.expose
class Client(object):
    def __init__(self, server):
        self.server = server

    def notify_event(self, filename):
        messagebox.showinfo("Notificação", f"Novo arquivo disponível: {filename}")

    def upload_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as file:
                content = file.read()
                print(content, filename)
            self.server.upload_file(filename, content)
            messagebox.showinfo("Upload", f"Arquivo '{filename}' enviado com sucesso.")

    def list_available_files(self):
        files = self.server.get_available_files()
        if files:
            file_list = "\n".join(files)
            messagebox.showinfo("Arquivos Disponíveis", f"Arquivos disponíveis:\n{file_list}")
        else:
            messagebox.showinfo("Arquivos Disponíveis", "Nenhum arquivo disponível.")

    def download_file(self):
        filename = simpledialog.askstring("Download", "Digite o nome do arquivo:")
        if filename:
            content, fileN = self.server.download_file(filename)
            print(fileN)
            if content:
                filepath = filedialog.asksaveasfilename( initialfile=fileN,filetypes = (("txtfiles","*.txt"),("all files","*.*")))
                serialized_content = content
                decoded_content = base64.b64decode(serialized_content['data'])
                with open(filepath, 'wb') as file:
                    file.write(decoded_content)
                messagebox.showinfo("Download", f"Arquivo '{fileN}' baixado com sucesso.")
            else:
                messagebox.showerror("Download", f"Arquivo '{fileN}' não encontrado.")

    def register_interest(self):
        filename = simpledialog.askstring("Registro de Interesse", "Digite o nome do arquivo:")
        if filename:
            duration = simpledialog.askinteger("Registro de Interesse", "Digite a duração em segundos:")
            if duration:
                self.server.register_interest(filename, self, duration)
                messagebox.showinfo("Registro de Interesse", f"Registro de interesse para o arquivo '{filename}' realizado com sucesso.")

    def cancel_interest(self):
        filename = simpledialog.askstring("Cancelamento de Interesse", "Digite o nome do arquivo:")
        if filename:
            self.server.cancel_interest(filename, self)
            messagebox.showinfo("Cancelamento de Interesse", f"Cancelamento de interesse para o arquivo '{filename}' realizado com sucesso.")





daemon = Pyro4.Daemon()
server = Pyro4.Proxy("PYRONAME:example.greeting")        
client = Client(server)
uri = daemon.register(client)

root = tk.Tk()

upload_button = tk.Button(root, text="Upload", command=client.upload_file)
upload_button.pack()

list_button = tk.Button(root, text="Listar Arquivos", command=client.list_available_files)
list_button.pack()

download_button = tk.Button(root, text="Download", command=client.download_file)
download_button.pack()

register_button = tk.Button(root, text="Registrar Interesse", command=client.register_interest)
register_button.pack()

cancel_button = tk.Button(root, text="Cancelar Interesse", command=client.cancel_interest)
cancel_button.pack()

root.geometry("400x300")

root.mainloop()