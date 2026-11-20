"""Profile pictures: the uploaded image becomes a new 256-pixel square JPEG, made here.

Nothing of the uploaded file is kept: the picture is decoded and drawn again, so photo details (camera, place,
date), extra data hidden in the file and anything that is not a picture are left behind. Only PNG, JPEG, WebP and
GIF (its first frame) are read; vector images (SVG) are refused, since they can carry scripts.
"""
import base64
import binascii
import io
import re

from PIL import Image, ImageOps, UnidentifiedImageError

SIZE = 256
MAX_UPLOAD = 4 * 1024 * 1024  # the page shrinks big photos before sending, so this is only a limit
MAX_PIXELS = 40_000_000  # a 40-megapixel image at most: bigger ones would take too much memory to decode
DATA_URL = re.compile(r"^data:image/(?:png|jpeg|webp|gif);base64,([A-Za-z0-9+/=\s]+)$")
FORMATS = {"PNG", "JPEG", "WEBP", "GIF"}


class PhotoError(Exception):
    """`code` is the message shown (err_photo_type, err_photo_size)."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def from_data_url(value):
    """The picture to keep, as JPEG bytes, from a data: URL the page sends."""
    match = DATA_URL.match(str(value or ""))
    if not match:
        raise PhotoError("err_photo_type")
    try:
        data = base64.b64decode("".join(match.group(1).split()), validate=True)
    except (binascii.Error, ValueError):
        raise PhotoError("err_photo_type")
    if len(data) > MAX_UPLOAD:
        raise PhotoError("err_photo_size")
    return make(data)


def make(data):
    try:
        img = Image.open(io.BytesIO(data))
        if img.format not in FORMATS:
            raise PhotoError("err_photo_type")
        width, height = img.size
        if width < 1 or height < 1 or width * height > MAX_PIXELS:
            raise PhotoError("err_photo_size")
        img.seek(0)
        img = ImageOps.exif_transpose(img)  # phone photos: turned the way they were taken
        if img.mode in ("RGBA", "LA", "P", "PA"):  # transparency on white
            img = img.convert("RGBA")
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.getchannel("A"))
            img = background
        img = ImageOps.fit(img.convert("RGB"), (SIZE, SIZE), Image.Resampling.LANCZOS)  # the middle square
        out = io.BytesIO()
        img.save(out, "JPEG", quality=85, optimize=True)
        return out.getvalue()
    except PhotoError:
        raise
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError, Image.DecompressionBombError):
        raise PhotoError("err_photo_type")
