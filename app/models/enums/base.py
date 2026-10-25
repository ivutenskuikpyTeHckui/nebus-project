from enum import StrEnum


class StrEnumModel(StrEnum):
    @classmethod
    def keys(cls) -> list[str]:
        return [item.name for item in cls]
