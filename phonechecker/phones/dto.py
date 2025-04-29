from dataclasses import dataclass
from pathlib import Path


@dataclass
class RegistryFileDTO:
    file: Path


# @dataclass(slots=True, frozen=True)
# class DEFPhoneDTO:
#     avs: int
#     from_: int
#     to: int
#     capacity: int
#     operator: str
#     region: str
#     territory: str
#     inn: str
