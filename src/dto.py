from dataclasses import dataclass
from typing import Optional


@dataclass
class DomainDTO:
    url: str
    id: Optional[int] = None
    surfed: bool = False


@dataclass
class DomainQueryDTO:
    url: Optional[str] = None
    id: Optional[int] = None
    surfed: Optional[bool] = None
