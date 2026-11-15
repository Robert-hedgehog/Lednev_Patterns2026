from typing import Dict, List, Type
from Src.Core.class_abstract import abstract


class common:
    """Набор общих статических методов рефлексии."""

    @staticmethod
    def get_fields(source: object) -> List[str]:
        """Получить список всех свойств-атрибутов объекта."""
        if source is None:
            return []
        cls = type(source)
        ignored = {"items", "unique_code", "type"}
        return [
            name for name in dir(cls)
            if not name.startswith("_") and name not in ignored
            and isinstance(getattr(cls, name, None), property)
        ]

    @staticmethod
    def __get_all_subclasses(base_cls: type) -> Dict[str, Type[abstract]]:
        """Рекурсивный сбор всех наследников базового класса."""
        result = {}
        for sub in base_cls.__subclasses__():
            result[sub.__name__] = sub
            result.update(common.__get_all_subclasses(sub))
        return result

    @staticmethod
    def domains(source: object) -> Dict[str, str]:
        """Получить словарь доступных ключей и их описаний из docstring."""
        methods = (
            getattr(source, name)
            for name in dir(source)
            if name.endswith("_key") and callable(getattr(source, name))
        )
        return {
            method(): (method.__doc__.strip().split("\n")[0] if method.__doc__ else method.__name__)
            for method in methods
        }

    @staticmethod
    def domain_models(source: object) -> Dict[str, Type[abstract]]:
        """Получить словарь ключей и соответствующих им классов моделей."""
        models = common.__get_all_subclasses(abstract)
        return {key: models[key] for key in common.domains(source) if key in models}