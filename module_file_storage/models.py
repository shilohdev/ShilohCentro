from django.conf import settings
from django.core.files.storage import default_storage
from functions.general.decorator import json_with_success, json_without_success


class FileStorageLocal:
    def __init__(self) -> None:
        self.storage = None

    def _authentication(self):
        if not self.storage:
            self.storage = default_storage

    def listdirectory(self, id=None) -> str:
        if not id:
            return json_without_success("Nenhum diretório enviado.")

        self._authentication()

        BASE_DIRECTORY = settings.BASE_DIR_PHOTO
        FILES_DIRECTORY = f"{BASE_DIRECTORY}/{id}"

        map_dirs = self.storage.listdir(FILES_DIRECTORY)
        if map_dirs:
            for key in map_dirs:
                if key:
                    if isinstance(key, list):
                        filename = key[0]
                        file_dir = f"{FILES_DIRECTORY}/{filename}".replace(BASE_DIRECTORY, "")
                        file_dir = f"{settings.SHORT_PLATAFORM}/docs/FotoPerfil{file_dir}"
                        print(file_dir)

                        return json_with_success(file_dir)
        
        return json_without_success("Nenhum arquivo encontrado.")