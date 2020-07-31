from lin.file import Uploader
import os

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from lin.core import File


class CaseUploader(Uploader):

    def __init__(self, files: list or FileStorage, config):
        super().__init__(files, config)
        self.config = config

    def upload(self):
        ret = []
        self.mkdir_if_not_exists()
        for single in self._file_storage:
            file_md5 = self._generate_md5(single.read())
            single.seek(0)
            exists = File.query.filter_by(md5=file_md5).first()
            if exists:
                ret.append({
                    "key": single.name,
                    "id": exists.id,
                    "path": exists.path,
                    "url": os.path.join(current_app.root_path, 'excel/upload', exists.path).replace('\\', '/')
                })
            else:
                absolute_path, relative_path, real_name = self._get_store_path(single.filename)
                secure_filename(single.filename)
                single.save(absolute_path)
                file = File.create_file(
                    name=real_name,
                    path=relative_path,
                    extension=self._get_ext(single.filename),
                    size=self._get_size(single),
                    md5=file_md5,
                    commit=True
                )
                ret.append({
                    "key": single.name,
                    "id": file.id,
                    "path": file.path,
                    "url": os.path.join(current_app.root_path, 'excel/upload', file.path).replace('\\', '/')
                })
        return ret
