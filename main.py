from selenium import webdriver
import time
import pickle
import cv2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from pytesseract import pytesseract
import re
import os
from tkinter import *

def init(username, password, browser):
    browser.get("https://i.napier.ac.uk/campusm/home#menu")

    # return cookies to not log in again
    if os.path.exists("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)

    time.sleep(3)
    # if not logged in
    if not browser.current_url.startswith("https://i.napier.ac.uk/"):
        try:
            WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            browser.find_element(By.XPATH, "//input[@type='email']").send_keys(username)
            browser.find_element(By.XPATH, "//input[@type='submit']").click()
            time.sleep(2)

            WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            browser.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
            browser.find_element(By.XPATH, "//input[@type='submit']").click()
            time.sleep(4)

            WebDriverWait(browser, 1000).until_not(EC.presence_of_element_located((By.CLASS_NAME, "displaySign")))

            WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))).click()
            time.sleep(2)
        except:
            return False

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "menu-option-31782")))
    time.sleep(3)
    browser.find_element(By.ID, "menu-option-31782").click()

    time.sleep(2)

    #print(elem.get_attribute("interHTML"))
    browser.switch_to.frame(1)
    # print(browser.page_source)

    try:
        browser.find_element(By.XPATH, "//button[text()='Check in']").click()
    except:
        return False
    return True


def findCheckIn(text):
    # patterns for XXX XXX and XXXXXX
    patterns = ["[A-Z0-9]{3} [A-Z0-9]{3}", "[A-Z0-9]{6}"]
    codes = []
    for pattern in patterns:
        code = re.findall(pattern, text)
        if not code == []:
            codes.append(code)

    return codes

def checkIn(code, browser):
    input = browser.find_element(By.XPATH, "//input[@type='text']")
    input.send_keys(code)

    submit = browser.find_element(By.XPATH, "//button[@type='submit']")
    if submit.is_enabled():
        submit.click()
        return True

    input.clear()

    return False




def main():
    username = "40618869@live.napier.ac.uk"
    password = ""

    app = Tk()
    app.title("shScanner")
    app.geometry("800x600")

    startScannImage = PhotoImage(file="Start Scan pic.png")
    startScannImage_label = Label(image=startScannImage)

    # Clickable body of the image
    scannButton = Button(app, image=startScannImage, borderwidth=0, command=app.destroy).pack(padx=0, pady=180)  #

    app.mainloop()

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    if not init(username, password, browser):
        browser.close()
        print("No check in available or failed to login")
        return



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
                time.sleep(5)
                break
        rval, frame = vc.read()

        key = cv2.waitKey(20)
        if key == 27:
            break

    if not os.path.exists("cookies.pkl"):
        pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
    cv2.destroyWindow("preview")
    vc.release()
    time.sleep(10)
    browser.close()

if __name__ == "__main__":
    main()