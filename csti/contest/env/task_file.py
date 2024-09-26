import os
from datetime import datetime

from csti.contest.task import Task


class TaskFile:
    """Управление файлов с заданием."""

    def __init__(self, baseDir: str, task: Task):
        self._baseDir = baseDir
        self._task = task

    @property
    def task(self) -> Task:
        return self._task

    @property
    def path(self) -> str:
        """Название файла."""
        file = str(self.task.id) + self.task.language.defaultfileExtension
        return os.path.join(self._baseDir, file)

    @property
    def exists(self) -> bool:
        """Проверяет существование файла."""
        return os.path.isfile(self.path)

    @property
    def modificationTime(self) -> datetime:
        """Возвращает дату последнего изменения файла."""
        return datetime.fromtimestamp(os.path.getmtime(self.path))

    def createTemplateCode(self) -> str:
        """Возвращает шаблонный код для задания."""

        code = self.task.language.comment + " " + self.task.name + "\n\n"
        if self.task.language.templateFile is not None:
            with open(self.task.language.templateFile, "r") as f:
                code += f.read()

        return code

    def create(self):
        with open(self.path, "w") as f:
            f.write(self.createTemplateCode())

    def remove(self):
        if self.exists:
            os.remove(self.path)
