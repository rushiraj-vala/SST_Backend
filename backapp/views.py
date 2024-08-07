import base64
import json
import os
from PIL import Image
from io import BytesIO
from .OCR import OCRManager

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .models import ImageModel

ocr_manager = OCRManager()


# Create your views here.

@csrf_exempt
def test_view(request):
    return JsonResponse({'message': 'Hello from Django server'})
    # return HttpResponse('Hello vala, You are at test view')


@csrf_exempt
def uploadImage(request):
    if request.method == 'POST' and request.FILES['image']:
        print('A request for upload image:', request)
        try:
            name = request.POST['name']
            image = request.FILES['image']  # upload the file at memory
            imageByte = image.read()  # read the file from memory
            if imageByte:
                image_df = ocr_manager.recognize(image=imageByte)
                image_df.drop(
                    columns=['level', 'page_num', 'block_num', 'par_num'], axis=1, inplace=True)
                image_df.dropna(inplace=True)
            else:
                print('file cannot be read or is empty')
            # print(image_df.to_json(orient="records"))
            image_instance = ImageModel(
                name=name, image=image, data=image_df.to_json(orient='records'), trash=False)
            print(image_instance)
            image_instance.save()
            return JsonResponse({'status': 'Success'})

        except Exception as e:
            print(str(e))
            return JsonResponse({'Error': str(e)})

    return JsonResponse({'Error': 'Invalid request'})


@csrf_exempt
def reRecognizeImage(request):
    if request.method == 'GET' and request.GET.get('name'):
        try:
            name = request.GET.get('name')
            print('recognize image for:', name)
            img = ImageModel.objects.get(name=name)
            print('Image found at: ', img.image.url)
            imageByte = img.image.read()
            if imageByte:
                image_df = ocr_manager.recognize(image=imageByte)
                image_df.drop(
                    columns=['level', 'page_num', 'block_num', 'par_num'], axis=1, inplace=True)
                image_df.dropna(inplace=True)
            else:
                print('file cannot be read or is empty')
            img.data = image_df.to_json(orient='records')
            response = {
                'df': img.data
            }
            print(image_df)
            print(image_df)
            return JsonResponse(response)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'name incorrect or not found'}, status=404)

    else:
        return JsonResponse({'Error': 'Invalid request'})

# Function for displaying list in admin

# def list_images(request):
#     images = ImageModel.objects.all()
#     image_data = [{'name': img.name, 'url': img.image.url, 'imageByte': str(img.image.read()),
#                    'uploaded_at': img.uploaded_at, 'data': img.data, 'trash': img.trash} for img in images]
#     return JsonResponse({'images': image_data})


@csrf_exempt
def listImages(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        nameList = request.GET.get('nameList')
        print('requested image: ', name)
        if name:
            try:
                img = ImageModel.objects.get(name=name)
                print('Image found at: ', img.image.url)
                byteImage = str(img.image.read())
                base64_string = base64.b64encode(byteImage).decode('utf-8')
                data_url = f"data:image/png;base64,{base64_string}"
                response = {
                    'url': img.image.url,
                    'imageByte': data_url,
                    'df': img.data,
                }
                img_data = img.image
                print(img.name)
                print(img_data.read())
                return JsonResponse(response)
            except ImageModel.DoesNotExist:
                return JsonResponse({'error': 'name not found'}, status=404)

        elif nameList:
            nameList = json.loads(nameList)
            try:
                imageNameList = nameList['imageList'].split(',')
                commandType = nameList['commandType']
                if commandType == 'trash':
                    print('Requesting to move to TRASH  this items ')
                    print(imageNameList)
                    for name in imageNameList:
                        print(ImageModel.objects.filter(
                            name=name).values())
                        item = ImageModel.objects.filter(
                            name=name)
                        item.update(trash=True)
                        print(item.values())
                    return JsonResponse({'Server-Success': 'imageList Recieved and deleted'})
                elif commandType == 'delete':
                    print('Requesting to PERMANENTLY delete following:')
                    print(imageNameList)
                    for name in imageNameList:
                        print(ImageModel.objects.filter(
                            name=name))
                        item = ImageModel.objects.filter(
                            name=name)
                        item.delete()
                    return JsonResponse({'Server-Success': 'imageList Recieved and deleted'})
            except:
                return JsonResponse({'Server-Error': 'Failed-imageList Recieved '})

        else:
            images = ImageModel.objects.all()
            if images:
                image_data = [{'name': img.name, 'url': img.image.url, 'df': img.data,
                               'uploaded_at': img.uploaded_at, 'trash': img.trash} for img in images]
                print('Returning following images:', images)
                return JsonResponse({'images': image_data})
            else:
                return JsonResponse({'Error': 'No Images in database'})

    return JsonResponse({'Error': 'Invalid Request'})


def processImageJSON(request):
    # convert bytes to string
    body_unicode = request.body.decode('utf-8')

    # now convert it to json
    body_data_json = json.loads(body_unicode)

    imgData = body_data_json.get('image')
    # print(imgData)
    format, imgstr = imgData.split(';base64,')
    # print(imgstr)
    ext = format.split('/')[-1]

    img = base64.b64decode(imgstr)
    print(type(img))
    filepath = os.path.join(os.path.dirname(
        __file__), f'media/images/test_image.{ext}')

    imagePIL = Image.open(BytesIO(img))
    imagePIL.save(filepath)
    imagePIL.show()
