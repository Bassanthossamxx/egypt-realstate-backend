from __future__ import annotations

import os
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage

from .models import StoredMedia


class DatabaseStorage(Storage):
    """Store uploaded media inside the database.

    The stored file is referenced by its storage name (e.g. "countries/<uuid>.webp").
    URLs are served via the Django route configured under MEDIA_URL.
    """

    def _open(self, name: str, mode: str = "rb"):
        obj = StoredMedia.objects.get(name=name)
        return ContentFile(obj.data, name=name)

    def _save(self, name: str, content) -> str:
        original_name = getattr(content, "name", "") or ""

        if not name:
            name = original_name

        name = (name or "").lstrip("/")

        base, ext = os.path.splitext(name)
        if not ext and original_name:
            _, ext = os.path.splitext(original_name)

        name = name if name else f"uploads/{uuid4().hex}{ext}"

        # Ensure uniqueness
        if StoredMedia.objects.filter(name=name).exists():
            name = f"{base}_{uuid4().hex}{ext}"

        # Read bytes
        data = content.read()
        size = len(data)
        content_type = getattr(content, "content_type", "") or ""

        StoredMedia.objects.update_or_create(
            name=name,
            defaults={
                "original_name": original_name,
                "content_type": content_type,
                "size": size,
                "data": data,
            },
        )

        return name

    def delete(self, name: str) -> None:
        StoredMedia.objects.filter(name=name).delete()

    def exists(self, name: str) -> bool:
        return StoredMedia.objects.filter(name=name).exists()

    def size(self, name: str) -> int:
        obj = StoredMedia.objects.only("size").get(name=name)
        return int(obj.size)

    def url(self, name: str) -> str:
        media_url = getattr(settings, "MEDIA_URL", "/media/")
        if not media_url.endswith("/"):
            media_url += "/"
        return f"{media_url}{name}"

    def get_available_name(self, name: str, max_length: int | None = None) -> str:
        name = (name or "").lstrip("/")
        if not name:
            name = f"uploads/{uuid4().hex}"

        if max_length and len(name) > max_length:
            base, ext = os.path.splitext(name)
            keep = max_length - len(ext) - 33  # '_' + uuid hex
            base = base[: max(1, keep)]
            name = f"{base}{ext}"

        if self.exists(name):
            base, ext = os.path.splitext(name)
            name = f"{base}_{uuid4().hex}{ext}"

        return name
