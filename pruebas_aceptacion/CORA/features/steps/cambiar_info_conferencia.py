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


@given(u'selecciono la conferencia "{nombre_conferencia}" presionando el boton Editar Conferencia')
def step_impl(context, nombre_conferencia):
    driver = context.driver

    try:
        # Esperar a que la tabla esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )
    except TimeoutException:
        raise Exception("No se encontró la tabla de conferencias.")

    try:
        # Buscar la fila que contenga el nombre exacto de la conferencia
        fila = driver.find_element(
            By.XPATH, f"//tr[td[normalize-space(text())='{nombre_conferencia}']]"
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fila)
        sleep(1)

        # Dentro de esa fila, encontrar el botón "Editar conferencia"
        boton_editar = fila.find_element(
            By.XPATH, ".//a[contains(text(), 'Editar conferencia')]"
        )
        boton_editar.click()

    except Exception as e:
        raise Exception(f"No se pudo seleccionar la conferencia '{nombre_conferencia}' para editar: {e}")


@given(u'modifico el nombre de la conferencia a "{nombre}"')
def step_impl(context, nombre):
    context.driver.find_element(By.NAME, 'nombre').clear()
    sleep(1)
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    sleep(1)


@when(u'presiono el botón "Guardar cambios"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/button').click()
    sleep(1)

@then(u'podre ver la conferencia con nombre "{conferencia}"')
def step_impl(context, conferencia):
    driver = context.driver
    
    # Esperar un poco por si la tabla tarda en cargar
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    
    # Buscar en todas las filas de la tabla si alguna contiene exactamente el nombre deseado
    filas = driver.find_elements(By.XPATH, "//table//tbody//tr")
    
    conferencia_encontrada = False
    for fila in filas:
        columnas = fila.find_elements(By.TAG_NAME, "td")
        if columnas and columnas[0].text.strip() == conferencia:
            conferencia_encontrada = True
            break

    assert conferencia_encontrada, "No se encontró la conferencia con nombre 'Conferencia Innovación 2025 - Edición'"



@given(u'modifico la duracion a "{mes}" meses, "{dia}" dias, "{hora}" horas y "{minuto}" minutos')
def step_impl(context, mes, dia, hora, minuto):
    context.driver.find_element(By.NAME, 'meses').clear()
    context.driver.find_element(By.NAME, 'dias').clear()
    context.driver.find_element(By.NAME, 'horas').clear()
    context.driver.find_element(By.NAME, 'minutos').clear()
    sleep(1)
    context.driver.find_element(By.NAME, 'meses').send_keys(mes)
    context.driver.find_element(By.NAME, 'dias').send_keys(dia)
    context.driver.find_element(By.NAME, 'horas').send_keys(hora)
    context.driver.find_element(By.NAME, 'minutos').send_keys(minuto)
    sleep(1)


@then(u'podre ver la conferencia de nombre "{nombre_conferencia}" con la fecha "{mes}" meses, "{dia}" dias, "{hora}" horas y "{minuto}" minutos')
def step_impl(context, nombre_conferencia, mes, dia, hora, minuto):
    driver = context.driver
    fecha_esperada = f"{mes} meses, {dia} días, {hora} horas, {minuto} minutos"
    print(f"Buscando la fecha: '{fecha_esperada}'")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    
    filas = driver.find_elements(By.XPATH, "//table//tbody//tr")

    conferencia_encontrada = False
    for fila in filas:
        columnas = fila.find_elements(By.TAG_NAME, "td")
        if not columnas:
            continue
        nombre = columnas[0].text.strip()
        fecha = columnas[1].text.strip()
        print(f"Comparando nombre: '{nombre}' y fecha: '{fecha}'")

        if nombre == nombre_conferencia and fecha == fecha_esperada:
            conferencia_encontrada = True
            break

    assert conferencia_encontrada, (
        f"No se encontró la conferencia con nombre '{nombre_conferencia}' "
        f"y fecha '{fecha_esperada}'"
    )


@given(u'hago clic en "Crear conferencia"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/a').click()
    sleep(1)

@when(u'presiono el botón "Crear conferencia"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/div/form/div/button').click()
    sleep(1)