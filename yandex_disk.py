import requests
import os
from tokens import YANDEX_TOKEN as ya_token


class YandexDiskUploader:
    def __init__(self, token):
        self.token = token
        self.root = ""
        # self.root = "Приложения/Netology_Upload"

    def get_headers(self):
        return {
            "Content-type": "application/json",
            "Authorization": "OAuth {}".format(self.token)
        }

    def get_upload_link(self, upload_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": upload_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file(self, upload_path, source_path):
        href = self.get_upload_link(self.root + upload_path).get("href", "")
        response = requests.put(href, data=open(source_path, "rb"))
        if response.status_code == 201:
            print(f"File {upload_path} succesfully downloaded")
        else:
            print(response.status_code)

    def upload_dir(self, upload_path, source_path):
        self.create_dir(upload_path)
        files = os.listdir(source_path)
        for file in files:
            if '.' not in file:
                self.upload_dir(upload_path + '/' + file, source_path + '/' + file)
            else:
                self.upload_file(upload_path + '/' + file, os.path.join(source_path, file))

    def check_dir(self, path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self.get_headers()
        params = {"path": self.root + path}
        response = requests.get(upload_url, headers=headers, params=params)
        if response.status_code == 200:
            print(f"Directory '{path}' exists")
            return True
        else:
            return False

    def create_dir(self, path):
        if not self.check_dir(path):
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
            headers = self.get_headers()
            params = {"path": self.root + path}
            response = requests.put(upload_url, headers=headers, params=params)
            if response.status_code == 201:
                print(f"Directory '{path}' succesfully created")
            else:
                print(response.status_code)

if __name__ == '__main__':
    uploader = YandexDiskUploader(ya_token)
    # filename = 'test.txt'
    # uploader.upload_file(filename, os.path.join(os.getcwd(), "files/", filename))
    dirname = 'files'
    uploader.upload_dir(dirname, os.path.join(os.getcwd(), dirname))
