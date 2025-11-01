"""Mock blockchain ledger using a simple hash chain for auditability."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class LedgerEntry:
    """Represents a block in the immutable ledger."""

    index: int
    data: Dict[str, str]
    previous_hash: str
    hash: str = field(init=False)

    def __post_init__(self) -> None:
        payload = json.dumps(self.data, sort_keys=True)
        self.hash = hashlib.sha256((payload + self.previous_hash + str(self.index)).encode()).hexdigest()


class AuditLedger:
    """Extremely small blockchain designed for audit logging."""

    def __init__(self) -> None:
        self.entries: List[LedgerEntry] = []
        self.append({"event": "genesis"})

    def append(self, data: Dict[str, str]) -> LedgerEntry:
        """Add a new entry to the ledger and return it."""

        previous_hash = self.entries[-1].hash if self.entries else "0" * 64
        entry = LedgerEntry(index=len(self.entries), data=data, previous_hash=previous_hash)
        self.entries.append(entry)
        return entry

    def as_dict(self) -> List[Dict[str, str]]:
        """Serialize the chain for dashboard visualisation."""

        return [
            {"index": entry.index, "hash": entry.hash[:16] + "...", "previous": entry.previous_hash[:16] + "...", "event": entry.data.get("event", "")}
            for entry in self.entries
        ]
