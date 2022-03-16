from django.shortcuts import render
import numpy as np

from .forms import ImageForm
from ml_models.classify_images import infer


def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            img_name = request.FILES['image']
            img_url = 'media/images/{}'.format(img_name)

            inference: infer.Inference = infer.Inference()
            probs: np.ndarray
            cls: int
            probs, cls = inference.run(img_name)

            dict_probs: dict = {
                cls_name: prob
                for cls_name, prob in zip(inference.class_names, probs)
            }
            return render(
                request,
                'classify_images/templates/image.html',
                {'img_url': img_url, 'probabilities': dict_probs, 'class': cls}
            )
    else:
        form = ImageForm()
        return render(
            request, 'classify_images/templates/index.html', {'form': form}
        )
