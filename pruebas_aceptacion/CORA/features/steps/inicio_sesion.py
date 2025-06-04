from behave import when, given, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

@given(u'ingreso como autor')
def step_impl(context):
    context.driver.maximize_window()
    context.driver.find_element(By.NAME, 'username').send_keys("autorP@autorP.com")
    context.driver.find_element(By.NAME, 'password').send_keys("P123456789")
    sleep(2)
    context.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    sleep(2)

@given(u'ingreso como organizador')
def step_impl(context):
    context.driver.maximize_window()
    context.driver.find_element(By.NAME, 'username').send_keys("organizadorP@organizadorP.com")
    context.driver.find_element(By.NAME, 'password').send_keys("P123456789")
    sleep(2)
    context.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    sleep(2)

@given(u'ingreso como revisor')
def step_impl(context):
    context.driver.maximize_window()
    context.driver.find_element(By.NAME, 'username').send_keys("revisorP@revisorP.com")
    context.driver.find_element(By.NAME, 'password').send_keys("P123456789")
    sleep(2)
    context.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    sleep(2)

@given(u'ingreso como administrador')
def step_impl(context):
    context.driver.maximize_window()
    context.driver.find_element(By.NAME, 'username').send_keys("adminP@adminP.com")
    context.driver.find_element(By.NAME, 'password').send_keys("P123456789")
    sleep(2)
    context.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    sleep(2)


