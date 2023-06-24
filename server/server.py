import Pyro4
import os
import time
import base64

def get_files_in_folder(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_name)
    return files

@Pyro4.expose
class FileServer(object):
    def __init__(self):
        self.files = {}  # Dicionário para armazenar os arquivos disponíveis
        self.interests = {}  # Dicionário para armazenar os interesses dos clientes

    def upload_file(self, filename, content):
        print(content)
        serialized_content = content
        decoded_content = base64.b64decode(serialized_content['data'])
        print(decoded_content, filename)
        
        filepath = os.path.join('arquivos', filename)
        with open(filepath, 'wb') as file:
            file.write(decoded_content)
        self.files

    def get_available_files(self):
        folder_path = 'arquivos'
        file_names = get_files_in_folder(folder_path)
        for file_name in file_names:
            print(file_name)
        return file_names

    def download_file(self, filename):
        filepath = os.path.join('arquivos', filename)
        with open(filepath, 'rb') as file:
            return (file.read(), filename)

    def register_interest(self, filename, client, duration):
        expiration_time = time.time() + duration
        if filename in self.interests:
            self.interests[filename].append((client, expiration_time))
        else:
            self.interests[filename] = [(client, expiration_time)]

    def cancel_interest(self, filename, client):
        if filename in self.interests:
            self.interests[filename] = [(c, t) for c, t in self.interests[filename] if c != client]

    def check_interests(self, filename):
        if filename in self.interests:
            current_time = time.time()
            for client, expiration_time in self.interests[filename]:
                if current_time <= expiration_time:
                    client.notify_event(filename)
               

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(FileServer())   # register the greeting maker as a Pyro object
ns.register("example.greeting", uri)

print("servidor rodando")
   # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls