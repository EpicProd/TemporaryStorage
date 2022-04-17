import datetime
import requests

from dataclasses import dataclass
from typing import Optional
from TemporaryStorage.providers import Provider, File, HostedFile


@dataclass
class ProviderInstance(Provider):
    def __provider_init__(self):
        self.provider = 'catbox'
        self.max_file_size = 200
        self.min_retention = None
        self.max_retention = None
        self.base_url = 'https://catbox.moe/'

    def check_file(self, file: File) -> bool:
        if (file.path.endswith('.jar') or
            file.path.endswith('.exe') or
            file.path.endswith('.cpl') or
            file.path.endswith('.scr') or
            file.path.endswith('.docx') or
            file.path.endswith('.doc')):
            return False
        if file.file_size > self.max_file_size:
            return False

        return True

    def upload(self, file: File) -> Optional[HostedFile]:
        req = requests.post(self.base_url + "/user/api.php", data={"reqtype": "fileupload", "userhash": ""}, files={"fileToUpload": open(file.path, 'rb')})

        if req.status_code != 200:
            return

        return HostedFile(
            provider=self.provider,
            url=req.text.split('\n')[0],
            retention_to=None
        )

