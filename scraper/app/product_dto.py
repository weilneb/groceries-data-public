from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config
from marshmallow import fields


@dataclass_json
@dataclass
class UnitPrice:
    price: str
    unit: str


def now_utc() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


@dataclass_json
@dataclass
class ProductDTO:
    id: str
    name: str
    category: str
    url: str
    price: float
    unit_price: Optional[UnitPrice] = None
    timestamp: datetime = field(default_factory=now_utc,
                                metadata=config(
                                    encoder=datetime.isoformat,
                                    decoder=datetime.fromisoformat,
                                    mm_field=fields.DateTime(format='iso')
                                )
                                )


if __name__ == '__main__':
    p1 = ProductDTO(id="a", name="abc", price=1.23, category="A", url="http://aaa.com")
    p2 = ProductDTO(id="b", name="xyz", price=1.23, category="B", url="http://bbb.com",
                    unit_price=UnitPrice(price="4.56", unit="1L"))
    print(p1, p2)
    print(p1.to_json())
    print(p2.to_json())
