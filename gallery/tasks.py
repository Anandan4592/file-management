import time

from celery import shared_task
from django.core.mail import send_mail
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Photo



def send_welcome_mail_realtime():
    time.sleep(5)
    send_mail(
        "Welcome!",
        "Thanks for uploading a photo! This mail was send in realtime.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )


@shared_task
def send_welcome_email_async(id):
    time.sleep(5)

    photo = Photo.objects.get(id=id)
    img = Image.open(photo.image.path)

        # Resize the image for the thumbnail (e.g., 150x150)
    thumbnail_size = (150, 150)
    img.thumbnail(thumbnail_size)  
    thumb_io = BytesIO()
    img.save(thumb_io, img.format)
    thumb_io.seek(0)
    thumbnail_name = f"thumbnail_{photo.id}.jpg"   
    photo.thumbnail.save(
            f"thumbnail/{thumbnail_name}", 
            ContentFile(thumb_io.getvalue()),
            save=True  
    )
    send_mail(
        "Welcome!",
        "Thanks for uploading a photo! This mail was send asynchronously.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )