"""
Utilities for provenance normalization and deduplication.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Dict, Iterable, List
from urllib.parse import urlparse

from ..adapters.base import DocumentRecord


def canonical_url(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return f"{parsed.scheme}://{netloc}{path}"


def enrich_provenance(records: Iterable[DocumentRecord]) -> List[DocumentRecord]:
    enriched: List[DocumentRecord] = []
    for record in records:
        canon = canonical_url(record.url)
        domain = urlparse(canon).netloc if canon else None
        record.metadata.setdefault("domain", domain)
        record.metadata.setdefault("canonical_url", canon or record.url)
        enriched.append(record)
    return enriched


def dedupe(records: Iterable[DocumentRecord]) -> List[DocumentRecord]:
    best_by_key: Dict[str, DocumentRecord] = {}
    for record in records:
        key = record.metadata.get("canonical_url") or canonical_url(record.url) or record.id
        existing = best_by_key.get(key)
        if not existing or (record.score or 0) > (existing.score or 0):
            best_by_key[key] = record
    return list(best_by_key.values())


def cluster_by_domain(records: Iterable[DocumentRecord]) -> Dict[str, List[DocumentRecord]]:
    buckets: Dict[str, List[DocumentRecord]] = defaultdict(list)
    for record in records:
        domain = record.metadata.get("domain") or "unknown"
        buckets[domain].append(record)
    return buckets


def provenance_hash(record: DocumentRecord) -> str:
    payload = record.metadata.get("canonical_url") or record.url or record.id
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def normalize(records: Iterable[DocumentRecord]) -> List[DocumentRecord]:
    enriched = enrich_provenance(records)
    return dedupe(enriched)
