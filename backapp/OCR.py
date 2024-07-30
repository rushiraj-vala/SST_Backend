"""
The Class for Optical Character Recognition
"""
import pytesseract as pyt
import os
from PIL import ImageTk, Image
from datetime import datetime
import io


class OCRManager():
    def __init__(self) -> None:
        pass

    def recognize(self, image):
        """
        inputs: image-raw byte

        output dataframe
        """
        with open('temp_image.png', 'wb') as f:
            f.write(image)

        return pyt.image_to_data('temp_image.png', output_type='data.frame')

    def imgTkTopng(self, TkImage):
        current_date = datetime.now()
        string_datetime = current_date.strftime("%Y%m%d_%H%M%S")+".png"
        new_file_path = os.path.join(os.getcwd(), string_datetime)
        print(new_file_path)
        imagePIL = ImageTk.getimage(TkImage)
        imagePIL.save(new_file_path, "PNG")

        img_byte_arr = io.BytesIO()
        imagePIL.save(img_byte_arr, format='PNG')
        imageByte = img_byte_arr.getvalue()

        imagePIL = Image.open(new_file_path)
        return imagePIL, imageByte, string_datetime
