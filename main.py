import cv2
from pytesseract import pytesseract
import re
import getpass
from tkinter import *

#Window Tkinter->
app = Tk()
app.title("shScanner")
app.geometry("800x600")
#->end

def findCheckIn(text):
    # patterns for XXX XXX and XXXXXX
    patterns = ["[A-Z0-9]{3} [A-Z0-9]{3}", "[A-Z0-9]{6}"]
    codes = []
    for pattern in patterns:
        code = re.findall(pattern, text)
        if not code == []:
            codes.append(code)
    return codes


def checkIn(code):
    # NOTE: application should be run directly through exe to avoid password echoing (execution through pycharm leads to cras)

    # username = "40618869@live.napier.ac.uk"
    # password = "no password :( "

    print("Enter student number")
    username = input() + "@live.napier.ac.uk"
    print("Enter password")
    password = getpass.getpass()


def main():
    #Button->
    #Image
    startScannImage = PhotoImage(file="C:/Users/Stepan/Documents/Programming/Python/hackathon - shScanner/SHscanner-master/Start Scan pic.png")
    startScannImage_label = Label(image=startScannImage)

    #Clickable body of the image
    scannButton = Button(app, image=startScannImage, borderwidth=0,command=app.destroy).pack(padx=0,pady= 180) #

    app.mainloop()
#->end
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    while rval:
        cv2.imshow("preview", frame)
        text = pytesseract.image_to_string(frame)
        codes = findCheckIn(text)
        if not codes == []:
            if checkIn(codes):
                break
        rval, frame = vc.read()

        key = cv2.waitKey(20)
        if key == 27:
            break

    cv2.destroyWindow("preview")
    vc.release()


if __name__ == "__main__":
    main()
