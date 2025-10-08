from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.api.contacts import _serialize_contact  # type: ignore  # noqa: E402
from app.domain import models  # type: ignore  # noqa: E402


def test_contact_serialization_includes_tags_list():
    contact = models.Contact(
        id=1,
        email="foo@example.com",
        full_name="Foo Bar",
        phone="123",
        tags={"vip": True, "beta": True},
        created_at=datetime.utcnow(),
    )
    payload = _serialize_contact(contact)
    assert sorted(payload.tags) == ["beta", "vip"]
    assert payload.employment is not None  # because vip
