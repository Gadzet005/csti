import os
from datetime import datetime

from csti.contest.task import Task
from csti.storage.config.config import Config


class TaskFile:
    """Управление файлов с заданием."""

    def __init__(self, config: Config, baseDir: str, task: Task):
        self._congig = config
        self._baseDir = baseDir
        self._task = task

    @property
    def task(self) -> Task:
        return self._task

    @property
    def name(self) -> str:
        name = self._congig.get("directories", "task-name-template")
        if not "#" in name:
            name += "#"
        number = f"{str(self.task.id)}{self.task.language.defaultfileExtension}"
        return name.replace("#", number)

    @property
    def path(self) -> str:
        """Название файла."""
        return os.path.join(self._baseDir, self.name)

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

    # TODO: добавить.
    def archivate(self):
        pass

    def unarchivate(self):
        pass
