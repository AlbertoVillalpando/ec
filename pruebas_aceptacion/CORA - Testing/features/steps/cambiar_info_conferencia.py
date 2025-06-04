from behave import when, given, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given(u'selecciono el listado de conferencias')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/aside/ul/li[1]/a/div').click()
    sleep(1)


@given(u'selecciono la conferencia "Prueba template" presionando el boton Editar Conferencia')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given selecciono la conferencia "Prueba template" presionando el boton Editar Conferencia')


@given(u'modifico el nombre de la conferencia a "Conferencia Innovación 2025 - Edición"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given modifico el nombre de la conferencia a "Conferencia Innovación 2025 - Edición"')


@when(u'presiono el botón "Guardar cambios"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When presiono el botón "Guardar cambios"')


@then(u'podre ver la conferencia con nombre "Conferencia Innovación 2025 - Edición"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then podre ver la conferencia con nombre "Conferencia Innovación 2025 - Edición"')


@given(u'selecciono la conferencia "Conferencia Innovación 2025 - Edición" presionando el boton Editar Conferencia')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given selecciono la conferencia "Conferencia Innovación 2025 - Edición" presionando el boton Editar Conferencia')


@given(u'modifico la duracion a "1" meses, "3" dias, "4" horas y "23" minutos')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given modifico la duracion a "1" meses, "3" dias, "4" horas y "23" minutos')


@then(u'podre ver la conferencia de nombre "Conferencia Innovación 2025 - Edición" con la fecha "1" meses, "3" dias, "4" horas y "23" minutos')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then podre ver la conferencia de nombre "Conferencia Innovación 2025 - Edición" con la fecha "1" meses, "3" dias, "4" horas y "23" minutos')