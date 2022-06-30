from django.db import models
from functions.general.decorator import json_with_success, json_without_success
from module_file_storage.models import FileStorageLocal


class PhotoServices:
    def __init__(self) -> None:
        self.storage = FileStorageLocal()

    def _get_photo_perfil(self, id: str):
        if not id:
            return json_without_success("Nenhum usuário enviado.")

        data = self.storage.listdirectory(id)

        return json_with_success(data)