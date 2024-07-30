from django.contrib import admin

# Register your models here.


class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at')
