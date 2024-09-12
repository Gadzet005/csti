from typing import Any, Callable, Type


def configCaseToCamel(name: str) -> str:
    """Конвертирует camel-case в CamelCase."""
    words = name.split("-")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def configField(
    name: str,
    type: Type,
    nestedIn: list | None = None,
    defaultValue: Any = None,
    serializer: Callable = lambda x: x,
    deserializer: Callable = lambda x: x,
):
    """ 
    Добавляет getter и setter для поля из конфига.
    ----------------------------------------------
    @param name: Имя поля в конфиге (в .yaml файле).
    @param type: Тип поля в конфиге.
    @param nestedIn: Список полей в которые данное поле вложено. \
        Например, для user.info.login: nestedIn = [user, info].
    @param defaultValue: Значение поля по умолчанию.
    @param serializer: Функция преобразования примитивного типа в объект.
    @param deserializer: Функция преобразования объекта обратно в примитивный тип.
    """

    attrName = configCaseToCamel(name)

    @property
    def attr(self):
        raw = self.get(name, nestedIn, defaultValue)
        return serializer(type(raw))

    @attr.setter
    def attr(self, value):
        self.set(name, type(deserializer(value)), nestedIn)

    def wrapper(cls):
        setattr(cls, attrName, attr)
        return cls

    return wrapper
