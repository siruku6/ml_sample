import base64
import cv2
from django.http import StreamingHttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'detect_expression/templates/index.html', {})


def start_webcam(request):
    if (request.method == 'POST'):
        try:
            frame_ = request.POST.get('image')
            frame_ = str(frame_)
            data = frame_.replace('data:image/jpeg;base64,', '')
            data = data.replace(' ', '+')
            imgdata = base64.b64decode(data)
            filename = 'some_image.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)
        except Exception as e:
            print(f'Error: {e}')

    return JsonResponse({'Json': data})


# ---------------------------------------------------------------
#   Under construnciton
#     These should deal live-stream.
# ---------------------------------------------------------------
def live():
    return lambda _: StreamingHttpResponse(
        generate_frame(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def generate_frame():
    capture = cv2.VideoCapture(0)
    while True:
        if not capture.isOpened():
            print('Capture is not opened.')
            break

        # カメラからフレーム画像を取得
        ret, frame = capture.read()
        if not ret:
            print('Failed to read frame.')
            break

        # TODO: ここで画像を加工する

        # フレーム画像をバイナリに変換
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        # フレーム画像のバイナリデータをブラウザに送る
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + byte_frame + b'\r\n\r\n'
        )
    capture.release()
