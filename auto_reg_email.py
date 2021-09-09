# -*- coding: utf8 -*-

import time
import random

import requests

from selenium import webdriver


thread_count = 1

SYMBOLS_LOW = 'abcdefghijklmnopqrstuvwxyz'
SYMBOLS_UP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '1234567890'


def check_account():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)

    url = "https://id.rambler.ru/login-20/mail-registration?back=https%3A%2F%2Fid.rambler.ru%2Faccount%2Fprofile"
    driver.get(url)

    # подгрузка формы
    time.sleep(3)
    form = driver.find_elements_by_tag_name('body')

    # почтовый ящик
    login = ''
    password = ''
    check_box_email = ''
    check_box_question = ''
    answer = ''

    # создание рандомного логина
    for i in range(7):
        login_symbol = random.choice(SYMBOLS_LOW)
        login_number = random.choice(NUMBERS)
        login += login_symbol
        login += login_number

    # создание рандомного пароля
    for i in range(7):
        pass_symbol_low = random.choice(SYMBOLS_LOW)
        pass_symbol_up = random.choice(SYMBOLS_UP)
        pass_number = random.choice(NUMBERS)
        password += pass_symbol_low
        password += pass_symbol_up
        password += pass_number

    for fr in form:
        # ввод логина
        fr.find_element_by_id('login').send_keys(login)
        # ввод пароля
        fr.find_element_by_id('newPassword').send_keys(password)
        # ввод пароля(повторно)
        fr.find_element_by_id('confirmPassword').send_keys(password)
        # рандомный выбор чекбокса почты
        fr.find_element_by_class_name('rui-Select-withBottomDropdown').click()
        checkbox_email = fr.find_element_by_class_name('rui-RelativeOverlay-content').text
        check_box_email += checkbox_email
        new_check = check_box_email.split("\n")
        new_check_random = random.choice(new_check)

        open_checkbox_mail = driver.find_elements_by_class_name('rui-RelativeOverlay-content')
        for item in open_checkbox_mail:
            for j in range(1, 7):
                result_mail = item.find_element_by_xpath(f'//*[@id="root"]/div/div[1]/div/article/form/div[1]/section/div/div/div[1]/div[2]/div/div[2]/div/div/div[{j}]').text
                if new_check_random in result_mail:
                    item.find_element_by_xpath(f'//*[@id="root"]/div/div[1]/div/article/form/div[1]/section/div/div/div[1]/div[2]/div/div[2]/div/div/div[{j}]').click()
                    break

        # рандомный выбор контрольного вопроса
        time.sleep(2)
        fr.find_element_by_id('question').click()
        checkbox_question = fr.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/article/form/div[3]/section/div/div/div[1]/div/div[2]').text
        check_box_question += checkbox_question
        new_check_question = checkbox_question.split("\n")
        new_check_random_question = random.choice(new_check_question)

        open_checkbox_question = driver.find_elements_by_class_name('rui-RelativeOverlay-content')
        for item in open_checkbox_question:
            for j in range(1, 14):
                result_mail = item.find_element_by_xpath(f'//*[@id="root"]/div/div[1]/div/article/form/div[3]/section/div/div/div[1]/div/div[2]/div/div/div[{j}]').text
                if new_check_random_question in result_mail:
                    item.find_element_by_xpath(f'//*[@id="root"]/div/div[1]/div/article/form/div[3]/section/div/div/div[1]/div/div[2]/div/div/div[{j}]').click()
                    break

        # поле "ответ на вопрос"
        for i in range(7):
            answer_random = random.choice(SYMBOLS_LOW)
            answer += answer_random
        fr.find_element_by_id('answer').send_keys(answer)

        # каптча 2.0
        res_post = requests.post(f'http://rucaptcha.com/in.php?key=4c68ef4e9afa9f0b963599a121952937&method=userrecaptcha&googlekey=6LeHeSkUAAAAANUvgxwQ6HOLXCT6w6jTtuJhpLU7&pageurl={url}')
        print(res_post.text)
        print_res = res_post.text
        res_post = print_res.replace("OK|", "")
        result = requests.get(f'http://rucaptcha.com/res.php?key=4c68ef4e9afa9f0b963599a121952937&action=get&id={res_post}')

        while result.text == "CAPCHA_NOT_READY":
            time.sleep(5)
            print(result.text)
            result = requests.get(f'http://rucaptcha.com/res.php?key=4c68ef4e9afa9f0b963599a121952937&action=get&id={res_post}')

        token = result.text
        new_token = token.replace("OK|", "")
        print(new_token)

        element = fr.find_element_by_class_name('g-recaptcha-response')
        driver.execute_script("arguments[0].removeAttribute('style')", element)

        fr.find_element_by_class_name('g-recaptcha-response').send_keys(new_token)

        # кнопка далее
        button = fr.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/article/form/button')
        driver.execute_script("arguments[0].removeAttribute('disabled')", button)
        driver.execute_script("arguments[0].removeAttribute('data-cerber-id')", button)
        driver.execute_script("arguments[0].removeAttribute('tabindex')", button)
        fr.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/article/form/button').click()


def main():
    check_account()


if __name__ == '__main__':
    main()