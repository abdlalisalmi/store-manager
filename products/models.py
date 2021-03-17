from store_manager.settings import DEBUG
from django.db import models
from django.conf import settings

from django.db.models.signals import post_delete 
from django.dispatch import receiver

# import sys
# from PIL import Image
# from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

import cloudinary

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

def changeImageName(instence, imageName):
    ext = imageName.split('.')[1]
    fullName = f"products/{instence.name}.{ext}"
    return fullName

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=changeImageName, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    box_quantity = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     self.image = self.compressImage(self.image)
    #     super(Product, self).save(*args, **kwargs)

    # def compressImage(self,uploadedImage):
    #     imageTemproary = Image.open(uploadedImage)
    #     if str(uploadedImage).split('.')[1].lower() == "png":
    #         imageTemproary = imageTemproary.convert('RGB')
    #     outputIoStream = BytesIO()
    #     imageTemproary.save(outputIoStream , format='JPEG', quality=40) 
    #     outputIoStream.seek(0)
    #     uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
    #     return uploadedImage

@receiver(post_delete, sender=Product)
def create_user_account(sender, instance, **kwargs):
    if sender and not settings.DEBUG:
        cloudinary.api.delete_resources([instance.image])
    
