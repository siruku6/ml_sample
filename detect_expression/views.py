import base64
import io

from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View

from PIL import Image, ImageDraw


class IndexView(View):
    def get(self, request):
        return render(request, 'detect_expression/templates/index.html', {})


def start_webcam(request):
    def frame_to_img(frame) -> Image.Image:
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

    def draw_box_and_text(image: Image.Image) -> None:
        draw = ImageDraw.Draw(image, 'RGB')
        draw.rectangle((50, 50, 200, 200), fill=None, outline=(255, 255, 255), width=5)

    def image_to_base64(image) -> bytes:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        bytes_arr: bytes = img_byte_arr.getvalue()
        return base64.b64encode(bytes_arr)

    def add_marker(base64_arr: bytes) -> bytes:
        return b'data:image/jpeg;base64,' + base64_arr

    if (request.method == 'POST'):
        try:
            frame_ = request.POST.get('image')
            image: Image.Image = frame_to_img(frame_)
            draw_box_and_text(image)
            base64_arr: bytes = image_to_base64(image)
            base64_with_marker: bytes = add_marker(base64_arr)

            # NOTE: not necessary but this can save image on OS
            # filename = './some_image2.jpg'
            # image.save(filename, quality=95)
        except Exception as e:
            print(f'Error: {e}')

        return HttpResponse(base64_with_marker, content_type='application/octet-stream')
