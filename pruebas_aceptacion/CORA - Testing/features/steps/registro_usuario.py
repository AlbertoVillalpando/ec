from behave import when, given, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

@given(u'ingreso mi nombre "{nombre}", apellido "{apellido}", correo "{correo}" y una contraseña "{contraseña}"')
def step_impl(context, nombre, apellido, correo, contraseña):
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.NAME, 'apellidos').send_keys(apellido)
    context.driver.find_element(By.NAME, 'email').send_keys(correo)
    context.driver.find_element(By.NAME, 'password1').send_keys(contraseña)
    sleep(1)


@given(u'confirmo la contraseña "{contraseña}"')
def step_impl(context, contraseña):
    context.driver.find_element(By.NAME, 'password2').send_keys(contraseña)
    sleep(1)


@given(u'selecciono el área de conocimiento "{area}"')
def step_impl(context, area):
    select_element = context.driver.find_element(By.NAME, 'area_conocimiento')  
    select = Select(select_element)
    sleep(1)
    select.select_by_visible_text(area)
    sleep(1)


@when(u'presiono el botón "Registrarse"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/form/button').click()
    sleep(1)



@then(u'debo de ver el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    div_mensaje = context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/h1')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"



@then(u'debo ver un mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    div_mensaje = context.driver.find_element(By.XPATH, '/html/body/div/form/div[3]/ul/li')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"
    sleep(2)
    context.driver.quit() 

