import traceback

from django.http import JsonResponse
# from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View

from PIL import Image
from torch import positive

from config import logger
import lib.image_processor as img_processor
from ml_models.detect_expression.detect import Detection


class IndexView(View):
    def get(self, request):
        # NOTE: load model file from S3 and set resnet18 model in advance
        #   by initializing this class
        Detection()

        return render(request, 'detect_expression/templates/index.html', {})


def start_webcam(request):
    if (request.method == 'POST'):
        try:
            frame_ = request.POST.get('image')
            image: Image.Image = img_processor.to_image(frame_)

            # NOTE: locate captured image on OS
            filename = f'{request.user.username}.jpg'
            image.save(f'media/images/{filename}', quality=95)

            detection_instance: Detection = Detection()
            # NOTE: This (run) needs that image is located on OS.
            positive_level: float = detection_instance.run(image_name=filename)
            logger.info(f'positive level: {positive_level}')

            img_processor.draw_box_and_text(image, text=f'Positive Level = {positive_level}')
            base64: str = img_processor.to_base64(image)
        except Exception:
            logger.error(traceback.format_exc())

        # NOTE: この書き方の時は、 $resultImg.setAttribute('src', data); で描画できる
        #   ただし、
        #       b'data:image/jpeg;base64,' + base64_arr
        #   とする必要がある (最後の`.decode()` は不要)
        # return HttpResponse(base64_with_marker, content_type='application/octet-stream')

        return JsonResponse(
            {
                'positive_level': positive_level,
                'image': base64,
            }
        )
