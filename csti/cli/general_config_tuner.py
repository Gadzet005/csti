import typing as t

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from csti.storage.config.tuner import ConfigTuner


class GeneralConfigTuner(ConfigTuner):
    """Класс для настройки глобального конфига приложения."""

    @t.override
    def _tune(self):
        featureChoices = [
            Choice(
                "enable-auto-tests",
                "Включить авто тесты",
                self.config["features", "enable-auto-tests"],
            ),
            Choice(
                "enable-auto-formatting",
                "Включить авто форматирование",
                self.config["features", "enable-auto-formatting"],
            ),
        ]

        enabledFeatures = inquirer.checkbox(  # type: ignore
            message="Настройка функций.", choices=featureChoices, vi_mode=True
        ).execute()

        for choice in featureChoices:
            self.config["features", choice.value] = choice.value in enabledFeatures

        self.config.save()
