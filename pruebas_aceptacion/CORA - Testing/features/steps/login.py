from behave import when, given, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

@given(u'que ingreso a la plataforma en la URL "{url}"')
def step_impl(context, url):
    context.driver = webdriver.Chrome()
    context.driver.get(url)
    sleep(2)


@given(u'ingreso mi correo "{username}" y una contraseña incorrecta "{password}"')
def step_impl(context, username, password):
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)
    sleep(2)


@when(u'presiono el botón "Iniciar sesión"')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    sleep(2)


@then(u'el sistema valida las credenciales y muestra un mensaje "{mensaje}"')
def step_impl(context, mensaje):
    div_mensaje = context.driver.find_element(By.CLASS_NAME, 'alert-danger')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"
    sleep(2)
    context.driver.quit() 


@then(u'el sistema valida las credenciales y accede al menu donde se muestra "{mensaje}"')
def step_impl(context, mensaje):
    div_mensaje = context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/h1')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"
    sleep(2)
    context.driver.quit() 

