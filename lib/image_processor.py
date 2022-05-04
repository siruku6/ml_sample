import base64
import io

from PIL import Image, ImageDraw, ImageFont


def to_image(frame):
    image: Image.Image = _frame_to_img(frame)
    return image


def _frame_to_img(frame) -> Image.Image:
    frame_str: str = str(frame)
    data: str = (
        frame_str
        .replace('data:image/jpeg;base64,', '')
        .replace(' ', '+')
    )
    base64_decoded: bytes = base64.b64decode(data)
    # filename = 'some_image.jpg'
    # with open(filename, 'wb') as f:
    #     f.write(base64_decoded)

    image: Image.Image = Image.open(io.BytesIO(base64_decoded))
    return image


def draw_box_and_text(image: Image.Image, text: str) -> None:
    draw: ImageDraw = ImageDraw.Draw(image, 'RGB')
    # draw.rectangle((50, 50, 200, 200), fill=None, outline=(255, 255, 255), width=5)

    # TODO: Alter font size later on.
    # font: ImageFont = ImageFont.truetype("arial.ttf", 4)
    draw.text((30, 30), text, fill=(255, 255, 255, 128))


def to_base64(image) -> str:
    base64_arr: bytes = _image_to_base64(image)
    base64_with_marker: str = _add_marker(base64_arr)
    return base64_with_marker


def _image_to_base64(image) -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    bytes_arr: bytes = img_byte_arr.getvalue()
    return base64.b64encode(bytes_arr)


def _add_marker(base64_arr: bytes) -> str:
    return 'data:image/jpeg;base64,' + base64_arr.decode()
