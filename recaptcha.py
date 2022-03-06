from http.cookiejar import Cookie
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from helper import readData
import codecs
from selenium.webdriver.chrome.options import Options
user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"



import random
import time
# for recaptcha solution
# import urllib
# import os
import requests
import speech_recognition # pip install SpeechRecognition
import pydub  # to convert mp3 to wav file
import ffmpy  # pip install ffmpy (and dependency with pydub also need to install sudo apt install ffmpeg (dorkar nai))


import ffmpeg
import csv

from selenium.webdriver.common.by import By


class CapSolution:
    def __init__(self):
        # self.driver = driver
        pass
    
    def delay(self):
        time.sleep(random.randint(2, 4))
    
    def download_audio(self, src):
        '''method to download audio from google captcha and read that'''
        rq = requests.get(src)
        filename = 'audio.mp3'
        with open(filename, 'wb') as f:
            f.write(rq.content)

    def multiple_captcha(self, browser):
        try:
            self.delay()
            time.sleep(3)
            multiple = browser.find_element(By.XPATH, "//div[@class='rc-audiochallenge-error-message']").text.strip()
            print(multiple)
            if multiple == 'Multiple correct solutions required - please solve more.':
                return True
        except:
            return False

    def play_to_verify(self, browser):
        # from here play button started
        try:
            time.sleep(2)
            self.delay()

            play_button = browser.find_element(By.XPATH, "//div[@class='rc-audiochallenge-play-button']/button")
            play_button.click()

            # get the audio which recorded after clicking on play button
            time.sleep(2)
            self.delay()
            audio_src = browser.find_element(By.XPATH, "//audio[@id='audio-source']").get_attribute('src')

            # function to download audio from the above source
            self.download_audio(audio_src)

            # convert mp3 to wav file
            audio = pydub.AudioSegment.from_mp3("audio.mp3")
            audio.export("audio.wav", format="wav")
            current_audio = speech_recognition.AudioFile("audio.wav")
            recognizer = speech_recognition.Recognizer()
            with current_audio as source:
                audio = recognizer.record(source)

            data = recognizer.recognize_google(audio)
            print('============================',data,'==========================')
            # now it is time to input the data to audio response key
            time.sleep(3)
            self.delay()
            browser.find_element(By.XPATH, "//input[@id='audio-response']").send_keys(data.lower())
            time.sleep(2)
            verify_button = browser.find_element(By.XPATH, "//button[@id='recaptcha-verify-button']")
            self.delay()
            time.sleep(3)
            verify_button.click()
            print('verification done successfully')
            return True
        except:
            print('An error occur to verify the Captcha')
            return False

    def capthasolution(self, browser):
        # get the captha frame
        self.delay()
        iframe = browser.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
        browser.switch_to.frame(iframe)
        self.delay()
        time.sleep(2)
        # get the checkbox and click
        browser.find_element(By.XPATH, "//span[@id='recaptcha-anchor']").click()

        try:
            #switch to deafault
            browser.switch_to.default_content()
            self.delay()
            challengeframe = browser.find_element(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")
            self.delay()
            # switch to audio frame
            browser.switch_to.frame(challengeframe)
            self.delay()
            click_audio = browser.find_element(By.XPATH, "//button[@class='rc-button goog-inline-block rc-button-audio']")
            self.delay()
            click_audio.click()  # clicked to audio challenge
           
            # switch to recaptcha audio control default_content
            # self.driver.switch_to.default_content()
            # from here play button started
            verify = self.play_to_verify(browser)
         
            while verify==False :
               print('The captha is verified ?: ',verify)
               return False

            # for the multiple captcha solution
            try:
                multip = self.multiple_captcha(browser)
                while multip:
                    self.delay()
                    verify = self.play_to_verify(browser)
                    if verify==False:
                        return False
            except:
                print('no multiplication')
                return True
            
            # clicking here to submit
            self.delay()
            browser.switch_to.default_content()
            time.sleep(5)

            print('Cap solution finished successfully')
            return True
            #browser.find_element(By.XPATH, "//div[@class='frm-button']/input").click()  # clicked on continue
        except:
            # clicking here to the submit
            print('CapSolution failed')
            self.delay()
            browser.switch_to.default_content()
            time.sleep(3)
            return False
            
            #browser.find_element(By.XPATH, "//div[@class='frm-button']/input").click()  # clicked on continue



if __name__ == '__main__':
    f = codecs.open('gene.txt', "w", "utf−8")
    for val in f :
        print(val)
    # row_number = int(18)
    # urlFromCsv=readData()
    # while row_number!=20:
    #     print(row_number)
    #     url = urlFromCsv[row_number][2]
    #     first = CapSolution()
    #     print(url)

    #     #for headless driveer       
    #     options = Options()
    #     #cookie
    #     # options.add_argument("--headless")
    #     options.add_argument(f'user-agent={user_agent_desktop}')
    #     options.add_argument("--window-size=1920,1080")
    #     options.add_argument('--ignore-certificate-errors')
    #     options.add_argument('--allow-running-insecure-content')
    #     options.add_argument("--disable-extensions")
    #     options.add_argument("--proxy-server='direct://'")
    #     options.add_argument("--proxy-bypass-list=*")
    #     options.add_argument("--start-maximized")
    #     options.add_argument('--disable-gpu')
    #     options.add_argument('--disable-dev-shm-usage')
    #     options.add_argument('--no-sandbox')
    #     driver = webdriver.Chrome(chrome_options=options)
        
    #     driver.get(url)
    #     #options=chrome_options
    
    #     time.sleep(10) #need time for loading the site

    #     result  = first.capthasolution(driver) #call algo captcha solution
    #     if result:
    #         print('okk done the job')
    #         time.sleep(5)
    #         filename = urlFromCsv[row_number][1]+'.html'.format()
    #         f = codecs.open(filename, "w", "utf−8")
    #         #obtain page source
    #         h = driver.page_source
    #         #write page source content to file
    #         f.writelines(h)
           
    #         driver.close()
    #         row_number+=1
    #     else:  driver.close()
        
