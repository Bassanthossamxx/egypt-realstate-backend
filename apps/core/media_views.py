from __future__ import annotations

import os

from django.http import Http404, HttpResponse

from .models import StoredMedia


def db_media_serve(request, path: str):
    """Serve database-stored media via /media/<path:path> URLs."""
    try:
        obj = StoredMedia.objects.get(name=path)
    except StoredMedia.DoesNotExist:
        raise Http404("Media not found")

    content_type = obj.content_type or "application/octet-stream"
    response = HttpResponse(obj.data, content_type=content_type)
    response["Content-Length"] = str(obj.size)

    filename = obj.original_name or os.path.basename(obj.name)
    response["Content-Disposition"] = f'inline; filename="{filename}"'

    return response
