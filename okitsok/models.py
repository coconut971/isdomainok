from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Money:
    value: float
    currency: str
    source: str
    kind: str
    url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DomainReport:
    domain: str
    status: str = "unknown"
    dns_status: str = "unknown"
    rdap_status: str = "not_checked"
    registrar: Optional[str] = None
    registered_at: Optional[str] = None
    expires_at: Optional[str] = None
    nameservers: List[str] = field(default_factory=list)
    for_sale: Optional[bool] = None
    marketplace: Optional[str] = None
    asking_price: Optional[Money] = None
    registration_price: Optional[Money] = None
    sale_url: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.asking_price:
            data["asking_price"] = self.asking_price.to_dict()
        if self.registration_price:
            data["registration_price"] = self.registration_price.to_dict()
        return data
