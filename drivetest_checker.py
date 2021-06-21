import time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib, ssl

opts = Options()
opts.headless = True
opts.silent = True
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome("DEFAULT", options=opts)  # Enter path to chromedriver on your computer i.e. C:/Users/marti/chromedriver/chromedriver.exe
browser.implicitly_wait(2.5)


def wait():
    input('Press Enter to continue.')


def login():
    browser.get('https://drivetest.ca/book-a-road-test/booking.html#/verify-driver')
    time.sleep(10)
    licence_form = browser.find_element_by_id('licenceNumber')
    expiry_form = browser.find_element_by_id('licenceExpiryDate')
    licence_form.send_keys('DEFAULT')  # Enter license number i.e. A0000-00000-00000
    expiry_form.send_keys('DEFAULT')  # Enter license expiry date i.e. 2020/01/28
    btn_submit = browser.find_element_by_id('regSubmitBtn')
    btn_submit.click()


def get_dates():
    time.sleep(3)
    btn_reschedule = browser.find_element_by_css_selector('button[data-ng-click="reschedule(appointment)"]')
    btn_reschedule.click()
    time.sleep(3)
    btn_reschedule_2 = browser.find_element_by_css_selector('button[title="reschedule"]')
    btn_reschedule_2.click()
    time.sleep(3)
    btn_continue = browser.find_element_by_xpath('//*[@id="booking-location"]/div/div/form/div[2]/div[2]/button')
    btn_continue.click()
    time.sleep(5)
    btn_next = browser.find_element_by_xpath('//*[@id="driver-info"]/div[1]/div[1]/div[1]/a[2]')
    months = []
    days = []
    for i in range(3):
        months.append(browser.find_element_by_css_selector('h3.ng-binding').text)
        days_avail = len(browser.find_elements_by_css_selector('a[class="date-link"]'))
        # days_unavail = len(browser.find_elements_by_css_selector('a[class="date-link disabled"]'))
        days.append(days_avail)
        btn_next.click()
        time.sleep(4)
    browser.close()
    return [days, months]


def check(days, months):
    for i in range(3):
        if days[i] > 0:
            month_avail = months[i]
            print("Test found in %s" % month_avail)
            return month_avail
    print("No tests available")
    return None

def send_email(month):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "DEFAULT"  # Enter sender address
    password = "DEFAULT" # Enter sender address password
    receiver_email = "DEFAULT"  # Enter receiver address
    message = """\
    Subject: Drive Test Available!

    A new drive test is available in %s!""" % month

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print('Email sent!')


def write_to_file(log_text):
    f = open("DEFAULT", "a") # Enter filepath to log file
    f.write(log_text)
    f.close()


def run():
    log_text = "\n" + str(datetime.datetime.now()) + "\n"
    login()
    days, months = get_dates()
    month_avail = check(days, months)
    to_string = ', '.join(str(e) for e in months) + '  ' + ', '.join(str(e) for e in days)
    log_text += to_string + "\n"
    if month_avail is None:
        log_text += "No tests available"
    else:
        send_email(month_avail)
        log_text += "Test found in %s" % month_avail
    log_text += "\n" + "Task complete" + "\n"
    write_to_file(log_text)


run()
exit()
