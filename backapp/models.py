from django.db import models

# Create your models here.


class ImageModel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    data = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    trash = models.BooleanField()

    def __str__(self) -> str:
        return self.name


# class DataFrame(models.Model):
#     imageName = models.OneToOneField(ImageModel, on_delete=models.CASCADE)
#     data = models.JSONField()
