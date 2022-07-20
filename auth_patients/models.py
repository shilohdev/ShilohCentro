from django.conf import settings
from django.core.files.storage import default_storage
import re


class Path_Patients: 
    def __init__(self, id=None, etype=None, file=None) -> None: 
        self.id = id
        self.etype = etype
        self.FILES = file

    def CreatePath(self):
        PATH = settings.BASE_DIR_DOCS + "/patients/docs_principais/{}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
        PATH_USER = PATH.format(self.id) # ADICIONANDO ID NO {} DE CIMA /\
        PATH_TYPES = PATH_USER + "/" + self.etype + "/" # AQUI ESTÁ INDO PARA O DIRETORIO: docs/patients/process/ID/tipo_do_arquivo
        arr_dir = []
        for name, file in self.FILES.items():
            file_name = default_storage.save(PATH_TYPES + file.name, file)
            arr_dir.append({
                "name": file.name,
                "path": PATH_TYPES + file.name
            })
        return True


class ViewDocsPatients:
    def __init__(self, id=None) -> None: 
        self.id = id

    def VerificaPath(self):
        try:
            keysLIST = []
            PATH = settings.BASE_DIR_DOCS + f"/patients/docs_principais/{self.id}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
            PATH_ORIGIN = f"/patients/docs_principais/{self.id}"
            DS = default_storage
            if DS.exists(PATH):
                LIST_TYPES = DS.listdir(PATH)
                if LIST_TYPES:
                    if len(LIST_TYPES) > 0:
                        arrLIST = []
                        for key in LIST_TYPES[0]:
                            arrLIST.append(key)

                        if arrLIST:
                            for paths in arrLIST:
                                arrLISTPATHS = DS.listdir(f"{PATH}/{paths}")
                                for key in arrLISTPATHS[1]:
                                    keysLIST.append({
                                        "type": str(paths),
                                        "type_desc": settings.LISTPATHTYPE.get(str(paths), ""),
                                        "name": key,
                                        "path": PATH_ORIGIN + f"/{paths}/{key}",
                                        "date_create": {
                                            "en": str(default_storage.get_created_time(f"{PATH}/{paths}/{key}").date()),
                                            "pt": str(default_storage.get_created_time(f"{PATH}/{paths}/{key}").strftime("%d/%m/%Y"))
                                        },
                                        "url": settings.SHORT_PLATAFORM + f"/docs/patients/docs_principais/{self.id}/{paths}/{key}"
                                    })
                                    print(keysLIST)
            return keysLIST

        except Exception as err:
            return "Não foi possível encontrar este paciente."