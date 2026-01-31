from __future__ import annotations

import re
from typing import Optional

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

from PIL import Image, UnidentifiedImageError

# --- Character class helpers ---
_LATIN_LETTER_RE = re.compile(r"[A-Za-z]")
# Broad Arabic blocks (letters + presentation forms).
_ARABIC_LETTER_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")


def _is_blank(value: Optional[str]) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def validate_english_text(value: str) -> None:
    """Validates that text is English/Latin-script oriented.

    - Allows any punctuation/markdown symbols.
    - Ensures it contains at least one Latin letter.
    - Rejects presence of Arabic letters.
    """
    if _is_blank(value):
        return

    if not isinstance(value, str):
        raise ValidationError(_("Value must be a string."))

    if _ARABIC_LETTER_RE.search(value):
        raise ValidationError(_("Please enter English text (no Arabic letters)."))

    if not _LATIN_LETTER_RE.search(value):
        raise ValidationError(_("Please enter English text (must include Latin letters)."))


def validate_arabic_text(value: str) -> None:
    """Validates that text is Arabic-script oriented.

    - Allows punctuation/markdown symbols.
    - Ensures it contains at least one Arabic letter.
    - Rejects presence of Latin letters.
    """
    if _is_blank(value):
        return

    if not isinstance(value, str):
        raise ValidationError(_("Value must be a string."))

    if _LATIN_LETTER_RE.search(value):
        raise ValidationError(_("Please enter Arabic text (no Latin letters)."))

    if not _ARABIC_LETTER_RE.search(value):
        raise ValidationError(_("Please enter Arabic text (must include Arabic letters)."))


_PHONE_STR_RE = re.compile(r"^\+?\d{7,20}$")


def validate_phone_number(value: str) -> None:
    """Phone number validation for CharField: digits with optional leading +."""
    if _is_blank(value):
        return

    if not isinstance(value, str):
        raise ValidationError(_("Phone number must be a string."))

    if not _PHONE_STR_RE.match(value.strip()):
        raise ValidationError(_("Enter a valid phone number (digits with optional leading '+')."))


def validate_http_https_url(value: str) -> None:
    """Flexible URL validation.

    Accepts:
    - http(s)://example.com/...
    - www.example.com/...
    - example.com/... (schemeless)

    Note: Django's URLField requires a scheme, so schemeless URLs should be stored
    in a CharField (we validate by prepending https:// for checking).
    """
    if _is_blank(value):
        return

    if not isinstance(value, str):
        raise ValidationError(_("URL must be a string."))

    raw = value.strip()
    lowered = raw.lower()

    # If scheme is missing, validate by prepending https://
    candidate = raw
    if lowered.startswith("www."):
        candidate = f"https://{raw}"
    elif not re.match(r"^[a-zA-Z][a-zA-Z0-9+\-.]*://", raw):
        candidate = f"https://{raw}"

    try:
        URLValidator()(candidate)
    except ValidationError:
        raise ValidationError(_("Enter a valid URL."))


def validate_markdown_text(value: str) -> None:
    """Lightweight markdown validator.

    This intentionally avoids requiring external markdown libraries.
    It mainly prevents invalid binary/null content.
    """
    if _is_blank(value):
        return

    if not isinstance(value, str):
        raise ValidationError(_("Markdown content must be a string."))

    if "\x00" in value:
        raise ValidationError(_("Content contains invalid null characters."))


IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

# Use this when the field explicitly allows multiple formats.
validate_image_extension = FileExtensionValidator(
    allowed_extensions=IMAGE_EXTENSIONS,
    message=_("Unsupported image extension. Allowed: %(allowed_extensions)s."),
)

# Default policy: images must be .webp unless the field is an exception.
validate_image_webp_only = FileExtensionValidator(
    allowed_extensions=["webp"],
    message=_("Only .webp images are allowed."),
)


def _validate_image_is_real_image(file_obj, *, allow_formats: list[str] | None = None) -> None:
    if file_obj is None:
        return

    # UploadedFile supports .seek/.tell.
    try:
        current_pos = file_obj.tell()
    except Exception:
        current_pos = None

    try:
        if current_pos is not None:
            file_obj.seek(0)

        img = Image.open(file_obj)
        fmt = (img.format or "").upper()
        img.verify()  # verifies file is not broken

        if allow_formats is not None:
            allowed = {f.upper() for f in allow_formats}
            if fmt not in allowed:
                raise ValidationError(
                    _(f"Only {', '.join(sorted(allowed))} images are allowed.")
                )
    except UnidentifiedImageError:
        raise ValidationError(_("Upload a valid image file."))
    except ValidationError:
        raise
    except Exception:
        # Avoid leaking internals; surface as validation error.
        raise ValidationError(_("Upload a valid image file."))
    finally:
        try:
            if current_pos is not None:
                file_obj.seek(current_pos)
        except Exception:
            pass


def validate_image_is_image(value) -> None:
    """Validate that the upload is a real image (any Pillow-supported format)."""
    _validate_image_is_real_image(value)


def validate_image_is_webp(value) -> None:
    """Validate that the upload is a real WebP image (content check)."""
    _validate_image_is_real_image(value, allow_formats=["WEBP"])
