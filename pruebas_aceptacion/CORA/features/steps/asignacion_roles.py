from behave import when, given, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given(u'selecciono el apartado Usuarios')
def step_impl(context):
    context.driver.find_element(By.XPATH, '/html/body/div/div/aside/ul/li[2]/a').click()
    sleep(1)


@given(u'al usuario con nombre "{usuario}" de apellido "{apellido}" activo el rol "{rol}"')
def step_impl(context, usuario, apellido, rol):
    driver = context.driver
    rol_nombre = rol.lower()

    try:
        tabla = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )
    except TimeoutException:
        raise Exception("No se encontró la tabla de usuarios en la página.")

    filas = tabla.find_elements(By.TAG_NAME, "tr")
    print(f"Filas encontradas: {len(filas)}")

    fila_usuario = None
    fila_index = None

    print("Usuarios encontrados en la tabla:")
    for i, fila in enumerate(filas, start=1):
        columnas = fila.find_elements(By.TAG_NAME, "td")
        if len(columnas) >= 2:
            nombre = columnas[0].text.strip()
            apellido_col = columnas[1].text.strip()
            print(f"{i}. Nombre: '{nombre}', Apellido: '{apellido_col}'")

            if nombre == usuario and apellido_col == apellido:
                fila_usuario = fila
                fila_index = i
        else:
            print(f"{i}. Fila con columnas insuficientes")

    if fila_usuario is None or fila_index is None:
        raise Exception(f"No se encontró la fila para el usuario {usuario} {apellido}")

    checkbox_name = f"roles_{fila_index}_{rol_nombre}"
    print(f"Buscando checkbox con name='{checkbox_name}'")

    try:
        checkbox = context.driver.find_element(By.NAME, checkbox_name)
        sleep(3)
        context.driver.execute_script("arguments[0].scrollIntoView();", checkbox)
        sleep(2)
        context.driver.find_element(By.NAME, checkbox_name).click()
    except:
        raise Exception(f"No se encontró el checkbox con name '{checkbox_name}' en la fila del usuario {usuario} {apellido}")


@when(u'presiono el botón Guardar Cambios')
def step_impl(context):
    driver = context.driver
    # Suponiendo que el botón tiene texto "Guardar Cambios"
    boton = driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar Cambios')]")
    sleep(3)
    context.driver.execute_script("arguments[0].scrollIntoView();", boton)
    sleep(2)
    boton.click()


@then(u'el sistema valida la selección y muestra en la columna ROL el texto "{rol}" del usuario "{nombre}" "{apellido}"')
def step_impl(context, rol, nombre, apellido):
    driver = context.driver

    try:
        # Esperar a que la tabla de usuarios esté visible
        tabla = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )
    except TimeoutException:
        raise Exception("No se encontró la tabla de usuarios en la página.")

    try:
        # Buscar la fila del usuario por nombre y apellido
        fila_usuario = driver.find_element(
            By.XPATH, f"//tr[td[contains(text(), '{nombre}')] and td[contains(text(), '{apellido}')]]"
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fila_usuario)
        sleep(1)
    except:
        raise Exception(f"No se encontró la fila del usuario {nombre} {apellido}")

    try:
        # Buscar la columna que contiene el rol
        columna_rol = fila_usuario.find_element(
            By.XPATH, ".//td[contains(@class, 'rol') or position()=4]"  # Ajusta el número si la columna cambia
        )
        texto_columna = columna_rol.text.strip()
        print(f"Texto en columna ROL: '{texto_columna}'")
        assert rol.lower() in texto_columna.lower(), f"Se esperaba ver '{rol}' pero se encontró '{texto_columna}'"
    except Exception as e:
        raise Exception(f"No se pudo validar la columna ROL del usuario {nombre} {apellido}: {e}")
