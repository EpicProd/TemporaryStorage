import datetime
import requests

from dataclasses import dataclass
from typing import Optional
from TemporaryStorage.providers import Provider, File, HostedFile


@dataclass
class ProviderInstance(Provider):
    def __provider_init__(self):
        self.provider = 'litterbox'
        self.max_file_size = 200
        self.min_retention = 3
        self.max_retention = 3
        self.base_url = 'https://litterbox.catbox.moe/'

    def __calc_retention_date__(self) -> datetime:
        return datetime.datetime.utcnow() + datetime.timedelta(days=self.max_retention)

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
        req = requests.post(self.base_url + "/resources/internals/api.php", data={"reqtype": "fileupload", "time": "72h"}, files={"fileToUpload": open(file.path, 'rb')})

        if req.status_code != 200:
            return

        return HostedFile(
            provider=self.provider,
            url=req.text.split('\n')[0],
            retention_to=self.__calc_retention_date__()
        )

