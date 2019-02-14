import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pyautogui
from tkinter import filedialog, Tk
import tkinter.messagebox as tm
import os
from urllib.request import urlopen

# pyinstaller --onefile --windowed --icon=app.ico easyapplybot_v06.5.py

class EasyApplyBot:

    MAX_APPLICATIONS = 3000

    def __init__(self,username,password, language, position, location, resumeloctn):

        print("\nWelcome to Easy Apply Bot\n")
        dirpath = os.getcwd()
        print("current directory is : " + dirpath)
        chromepath = dirpath + '/assets/chromedriver.exe'
        #foldername = os.path.basename(dirpath)
        #print("Directory name is : " + foldername)

        self.language = language
        self.options = self.browser_options()
        #self.browser = webdriver.Chrome()
        #self.browser = webdriver.Chrome(executable_path = "C:/chromedriver_win32/chromedriver.exe")
 #       self.browser = webdriver.Chrome(chrome_options=self.options, executable_path = chromepath)
        self.browser = webdriver.Chrome(executable_path = r"/Users/phuphanmbp17/assets/chromedriver.exe")

        self.start_linkedin(username,password)


    def browser_options(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("user-agent=Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393")
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        #options.add_argument('--disable-gpu')
        #options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        return options

    def start_linkedin(self,username,password):
        print("\nLogging in.....\n \nPlease wait :) \n ")
        self.browser.get("https://www.linkedin.com/")
        try:
            user_field = self.browser.find_element_by_class_name("login-email")
            pw_field = self.browser.find_element_by_class_name("login-password")
            login_button = self.browser.find_element_by_id("login-submit")
            user_field.send_keys(username)
            user_field.send_keys(Keys.TAB)
            time.sleep(1)
            pw_field.send_keys(password)
            time.sleep(1)
            login_button.click()
        except TimeoutException:
            print("TimeoutException! Username/password field or login button not found")


    def wait_for_login(self):
        if self.language == "en":
             title = "Sign In to LinkedIn"
        elif self.language == "es":
             title = "Inicia sesión"
        elif self.language == "pt":
             title = "Entrar no LinkedIn"

        time.sleep(1)

        while True:
            if self.browser.title != title:
                print("\nStarting LinkedIn bot\n")
                break
            else:
                time.sleep(1)
                print("\nPlease Login to your LinkedIn account\n")

    def fill_data(self, position, location, resumeloctn):
        self.browser.set_window_size(0, 0)
        self.browser.set_window_position(2000, 2000)
        os.system("reset")

        self.position = position
        self.location = "&location=" + location
        self.resumeloctn = resumeloctn
        print(self.resumeloctn)


    def start_apply(self, position, location, resumeloctn):
        #self.wait_for_login()
        self.fill_data(position, location, resumeloctn)
        self.applications_loop()

    def applications_loop(self):

        count_application = 0
        count_job = 0
        jobs_per_page = 0

        os.system("reset")

        print("\nLooking for jobs.. Please wait..\n")

        self.browser.set_window_position(0, 0)
        self.browser.maximize_window()
        self.browser, _ = self.next_jobs_page(jobs_per_page)
        print("\nLooking for jobs.. Please wait..\n")

        submitButton = self.browser.find_element_by_class_name("jobs-search-dropdown__trigger-icon")
        submitButton.click()
        submitButton = self.browser.find_element_by_class_name("jobs-search-dropdown__option")
        submitButton.click()

        while count_application < self.MAX_APPLICATIONS:
            # sleep to make sure everything loads, add random to make us look human.
            time.sleep(random.uniform(3.5, 6.9))
            self.load_page(sleep=1)
            page = BeautifulSoup(self.browser.page_source, 'lxml')

            jobs = self.get_job_links(page)

            if not jobs:
                print("Jobs not found")
                break

            for job in jobs:
                time.sleep(random.uniform(3.5, 6.9))
                count_job += 1
                job_page = self.get_job_page(job)

                if self.got_easy_apply(job_page):
                    string_easy = "* has Easy Apply Button"
                    xpath = self.easy_apply_xpath()
                    self.click_button(xpath)
                    self.send_resume()
                    count_application += 1

                else:
                    string_easy = "* Doesn't have Easy Apply Button"

                position_number = str(count_job + jobs_per_page)
                print(f"\nPosition {position_number}:\n {self.browser.title} \n {string_easy} \n")



                if (count_application+1) % 20 == 0:
                    print('\n\n****************************************\n\n')
                    print('Time for a nap - see you in 10 min..')
                    print('\n\n****************************************\n\n')
                    time.sleep (600)

                if count_job == len(jobs):
                    jobs_per_page = jobs_per_page + 25
                    count_job = 0
                    print('\n\n****************************************\n\n')
                    print('Going to next jobs page, YEAAAHHH!!')
                    print('\n\n****************************************\n\n')
                    self.avoid_lock()
                    self.browser, jobs_per_page = self.next_jobs_page(jobs_per_page)

        self.finish_apply()

    def get_job_links(self, page):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')
            if url:
                if '/jobs/view' in url:
                    links.append(url)
        return set(links)

    def get_job_page(self, job):
        root = 'www.linkedin.com'
        if root not in job:
            job = 'https://www.linkedin.com'+job
        self.browser.get(job)
        self.job_page = self.load_page(sleep=0.5)
        return self.job_page

    def got_easy_apply(self, page):
       # button = page.find("button", class_="jobs-apply-button artdeco-button jobs-apply-button--top-card artdeco-button--3 ember-view")
        button = page.find("button", class_="jobs-apply-button--top-card artdeco-button--3 artdeco-button--primary jobs-apply-button artdeco-button ember-view")
        return len(str(button)) > 4

    def get_easy_apply_button(self):
        button_class = "jobs-s-apply--fadein inline-flex jobs-s-apply ember-view"
        button = self.job_page.find("div", class_=button_class)
        return button

    def easy_apply_xpath(self):
        button = self.get_easy_apply_button()
        print("\nbutton\n")

        button_inner_html = str(button)
        list_of_words = button_inner_html.split()
        next_word = [word for word in list_of_words if "ember" in word and "id" in word]
        ember = next_word[0][:-1]
        xpath = '//*[@'+ember+']/button'
        return xpath

    def click_button(self, xpath):
        triggerDropDown = self.browser.find_element_by_xpath(xpath)
        time.sleep(0.5)
        try:
            triggerDropDown.click()
        except WebDriverException:
            print("WebDriverException")
        time.sleep(1)

    def send_resume(self):
        # self.browser.find_element_by_xpath('//*[@id="file-browse-input"]').send_keys(self.resumeloctn)
        submit_button = None
        time.sleep(3)

        try:
            if self.browser.find_element_by_xpath("//*[contains(text(), 'Submit application')]"):
                submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Submit application')]")
                # submit_button = self.browser.find_element_by_class_name("continue-btn")
                submit_button.click()
        except NoSuchElementException:
            print("Wrong")
        time.sleep(random.uniform(1.5, 2.5))
        # submit_button = self.browser.find_element_by_class_name("continue-btn");

        # while not submit_button:
        #     if language == "en":
        #         submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Submit application')]")
        #     elif language == "es":
        #         submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Enviar solicitud')]")
        #     elif language == "pt":
        #         submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Enviar candidatura')]")
        time.sleep(random.uniform(1.5, 2.5))

    def load_page(self, sleep=1):
        scroll_page = 0
        while scroll_page < 4000:
            self.browser.execute_script("window.scrollTo(0,"+str(scroll_page)+" );")
            scroll_page += 200
            time.sleep(sleep)

        if sleep != 1:
            self.browser.execute_script("window.scrollTo(0,0);")
            time.sleep(sleep * 3)

        page = BeautifulSoup(self.browser.page_source, "lxml")
        return page

    def avoid_lock(self):
        x, _ = pyautogui.position()
        pyautogui.moveTo(x+200, None, duration=1.0)
        pyautogui.moveTo(x, None, duration=0.5)
        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(0.5)
        pyautogui.press('esc')

    def next_jobs_page(self, jobs_per_page):
        self.browser.get(
            "https://www.linkedin.com/jobs/search/?f_LF=f_AL%2Cf_EA&keywords=" +
            self.position + self.location + "&start="+str(jobs_per_page))
        self.avoid_lock()
        self.load_page()
        return (self.browser, jobs_per_page)

    def finish_apply(self):
        self.browser.close()

### if __name__ == '__main__':
