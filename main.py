import cv2
from PIL import Image
from pytesseract import pytesseract

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
while rval:
    cv2.imshow("preview", frame)
    #cv2.imwrite("image.jpg", frame)
    #img = Image.open("image.jpg")
    text = pytesseract.image_to_string(frame)
    print(text[:-1])
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyWindow("preview")
vc.release()