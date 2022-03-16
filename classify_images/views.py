from django.shortcuts import render
from .forms import ImageForm


def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            img_name = request.FILES['image']
            img_url = 'media/images/{}'.format(img_name)

            return render(request, 'classify_images/templates/image.html', {'img_url': img_url})
    else:
        form = ImageForm()
        return render(
            request, 'classify_images/templates/index.html', {'form': form}
        )
