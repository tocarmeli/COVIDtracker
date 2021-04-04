# Sends a weekly email giving an update on cases, deaths, and vaccine info in MA
# Information is gathered using NYT's COVID-19 tracking page

import smtplib
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('https://www.nytimes.com/interactive/2021/us/massachusetts-covid-cases.html') # website url

# amount of people who have received the first dose of the vaccine
def get_first_dose():
    first_dose = browser.find_element_by_xpath('//*[@id="svelte"]/main/div[2]/div[2]/div[3]/section[1]/div/div[2]/div[1]')
    return first_dose.get_attribute('innerHTML')

# gets the amount of people who have been fully vaccinated
def get_fully_vaccinated():
    fully_vaccinated = browser.find_element_by_xpath('//*[@id="svelte"]/main/div[2]/div[2]/div[3]/section[1]/div/div[1]/div[1]')
    return fully_vaccinated.get_attribute('innerHTML')

# gets the total cases
def get_cases():
    cases = browser.find_element_by_xpath('//*[@id="svelte"]/main/div[2]/div[2]/div[2]/section[1]/div[3]/table/tbody/tr[1]/td[4]')
    return cases.get_attribute('innerHTML')

# gets the total number of deaths
def total_deaths():
    deaths = browser.find_element_by_xpath('//*[@id="svelte"]/main/div[2]/div[2]/div[2]/section[1]/div[3]/table/tbody/tr[4]/td[4]')
    return deaths.get_attribute('innerHTML')
    

# sends email to user
def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    total_cases = 'Total cases: ' + get_cases()
    total_first_dose = 'Total people who have received their first dose: ' + str(get_first_dose())
    total_vaxxed = 'People who have been fully vaccinated: ' + str(get_fully_vaccinated())
    tot_deaths = 'Total deaths: ' + str(total_deaths())
    stats = [total_cases, tot_deaths, total_first_dose, total_vaxxed]
    server.login('', 'pgluytbbrxyszkyk') # recipient email goes in the first pair of single quotes
    subject = 'COVID-19 Update For ' + str(date.today())
    
    body = 'This week in MA: \n'
    for stat in stats:
        body += stat + '\n'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('', '', msg) # recepient email goes in the first two pairs of single quotes

    print('Email has been sent')
    server.quit()

send_email()