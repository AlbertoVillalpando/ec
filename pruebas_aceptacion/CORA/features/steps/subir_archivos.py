import os
from behave import when, given, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given(u'selecciono el listado de conferencias como autor')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/aside/ul/li[2]/a/div').click()
    sleep(1)


@given(u'selecciono la conferencia "{nombre_conferencia}" presionando el boton Subir')
def step_impl(context, nombre_conferencia):
    driver = context.driver

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
        if nombre == nombre_conferencia:
            # Buscar el botón "Subir" dentro de esa fila
            try:
                boton_subir = fila.find_element(By.XPATH, ".//a[contains(text(), 'Subir')]")
                boton_subir.click()
                conferencia_encontrada = True
                break
            except Exception as e:
                raise AssertionError(f"Se encontró la conferencia '{nombre}', pero no se pudo hacer clic en el botón 'Subir'. Error: {e}")

    assert conferencia_encontrada, "No se encontró la conferencia con nombre 'Prueba template'"



@given(u'subo el archivo .zip')
def step_impl(context):
    driver = context.driver

    # Ruta absoluta al archivo ZIP de prueba
    zip_path = os.path.abspath("features/files/fontedit.zip")

    # Espera a que el input de tipo archivo esté visible
    input_file = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "archivo"))
    )

    # Subir archivo
    input_file.send_keys(zip_path)



@when(u'presiono el botón Subir')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/form/div[2]/button').click()
    sleep(1)


@then(u'el sistema muestra el boton "Archivo" en la conferencia "{nombre_conferencia}"')
def step_impl(context, nombre_conferencia):
    driver = context.driver

    # Esperar la tabla con las conferencias
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )


    # Verificar que ahora aparece el botón "Archivo" en la fila de la conferencia
    filas = driver.find_elements(By.XPATH, "//table//tbody//tr")
    archivo_encontrado = False
    for fila in filas:
        columnas = fila.find_elements(By.TAG_NAME, "td")
        if not columnas:
            continue

        nombre = columnas[0].text.strip()
        if nombre == nombre_conferencia:
            try:
                boton_archivo = fila.find_element(By.XPATH, ".//a[contains(text(), 'Archivo')]")
                archivo_encontrado = True
                break
            except:
                archivo_encontrado = False
                break

    assert archivo_encontrado, f"Después de subir el archivo, no se encontró el botón 'Archivo' para la conferencia '{nombre_conferencia}'"


@given(u'subo el archivo .jpeg')
def step_impl(context):
    driver = context.driver

    # Ruta absoluta al archivo jpeg de prueba
    zip_path = os.path.abspath("features/files/imagen.jpg")

    # Espera a que el input de tipo archivo esté visible
    input_file = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "archivo"))
    )

    # Subir archivo
    input_file.send_keys(zip_path)


@then(u'el sistema permanece en la misma vista')
def step_impl(context):
    try:
        # Esperamos hasta 5 segundos a que aparezca el botón "Subir"
        boton_subir = WebDriverWait(context.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/div/div/form/div[2]/button"))
        )
        assert boton_subir.is_displayed(), "El botón 'Subir' no está visible, por lo tanto, no estamos en la misma vista."
    except Exception as e:
        raise AssertionError(f"No se encontró el botón 'Subir'. No se permanece en la misma vista. Detalles: {e}")
