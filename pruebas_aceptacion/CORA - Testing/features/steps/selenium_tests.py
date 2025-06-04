
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def login_as_admin():
    """
    Inicia sesión como administrador en la plataforma.

    Este método navega a la página de login y proporciona las credenciales 
    de administrador para acceder a la plataforma de administración.
    """
    driver.get("http://127.0.0.1:8000/login")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("adminpassword")
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(2)

def test_change_deadline_success():
    """
    Verifica que el cambio de fecha de envío sea exitoso.

    Este escenario cubre el caso en el que el administrador ingresa a la plataforma,
    selecciona una conferencia existente, cambia la fecha de envío a una posterior 
    y guarda los cambios. Verifica que el sistema muestre el mensaje de éxito.
    """
    login_as_admin()
    driver.get("http://127.0.0.1:8000/admin/conferencias")
    driver.find_element(By.LINK_TEXT, "Editar conferencia").click()
    driver.find_element(By.NAME, "fecha_envio").clear()
    driver.find_element(By.NAME, "fecha_envio").send_keys("2025-12-31")
    driver.find_element(By.ID, "guardar_cambios").click()
    time.sleep(2)
    assert "Fecha de envío actualizada correctamente" in driver.page_source

def test_change_deadline_failure():
    """
    Verifica que el cambio de fecha de envío falle si la nueva fecha es menor que la actual.

    Este escenario cubre el caso en el que el administrador intenta cambiar la fecha de 
    envío a una fecha anterior a la actual y verifica que el sistema muestra un error.
    """
    login_as_admin()
    driver.get("http://127.0.0.1:8000/admin/conferencias")
    driver.find_element(By.LINK_TEXT, "Editar conferencia").click()
    driver.find_element(By.NAME, "fecha_envio").clear()
    driver.find_element(By.NAME, "fecha_envio").send_keys("2020-01-01")
    driver.find_element(By.ID, "guardar_cambios").click()
    time.sleep(2)
    assert "La fecha debe ser mayor o igual a la actual" in driver.page_source

def test_update_conference_info_success():
    """
    Verifica que la modificación de la información de una conferencia sea exitosa.

    Este escenario cubre el caso en el que el administrador selecciona una conferencia
    para editar, cambia su nombre y guarda los cambios. Verifica que el sistema redirija 
    al listado actualizado con la nueva información.
    """
    login_as_admin()
    driver.get("http://127.0.0.1:8000/admin/conferencias")
    driver.find_element(By.LINK_TEXT, "Editar conferencia").click()
    driver.find_element(By.NAME, "nombre_conferencia").clear()
    driver.find_element(By.NAME, "nombre_conferencia").send_keys("Conferencia Innovación 2025 - Edición")
    driver.find_element(By.ID, "confirmar_cambios").click()
    time.sleep(2)
    assert "Conferencia Innovación 2025 - Edición" in driver.page_source

def test_update_conference_info_failure():
    """
    Verifica que el sistema muestre un error si ocurre un fallo al guardar la conferencia.

    Este escenario simula un error al intentar guardar los cambios en la conferencia 
    y verifica que el sistema muestre el mensaje de error correspondiente.
    """
    login_as_admin()
    driver.get("http://127.0.0.1:8000/admin/conferencias")
    driver.find_element(By.LINK_TEXT, "Editar conferencia").click()
    driver.find_element(By.NAME, "nombre_conferencia").clear()
    driver.find_element(By.NAME, "nombre_conferencia").send_keys("Conferencia Innovación 2025 - Edición")
    driver.find_element(By.ID, "confirmar_cambios").click()
    time.sleep(2)
    # Simula un error en la base de datos
    assert "Error al guardar los cambios" in driver.page_source

def test_create_conference_success():
    """
    Verifica que la creación de una conferencia sea exitosa.

    Este escenario cubre el caso en el que el administrador ingresa a la plataforma,
    selecciona la opción para crear una conferencia, llena el formulario con los datos 
    requeridos y guarda los cambios. Verifica que el sistema cree la conferencia 
    y redirija al listado con la nueva conferencia visible.
    """
    login_as_admin()
    driver.get("http://127.0.0.1:8000/admin/conferencias")
    driver.find_element(By.LINK_TEXT, "Crear conferencia").click()
    driver.find_element(By.NAME, "nombre_conferencia").send_keys("Conferencia Innovación 2025")
    driver.find_element(By.NAME, "area_conocimiento").send_keys("Ciencias")
    driver.find_element(By.NAME, "fecha_envio").send_keys("2025-06-30")
    driver.find_element(By.NAME, "numero_revisores").send_keys("3")
    driver.find_element(By.NAME, "criterios_evaluacion").send_keys("Criterio 1, Criterio 2")
    driver.find_element(By.ID, "crear_conferencia").click()
    time.sleep(2)
    assert "Conferencia Innovación 2025" in driver.page_source

def test_create_conference_name_duplicate():
    """
    Verifica que la creación de una conferencia falle si el nombre ya está registrado.

    Este escenario cubre el caso en el que el administrador intenta crear una conferencia 
    con un nombre ya existente en la base de datos. El sistema debe mostrar un error.
    """
    login_as_admin()
    driver.get("http://127.0.0.1:8000/admin/conferencias")
    driver.find_element(By.LINK_TEXT, "Crear conferencia").click()
    driver.find_element(By.NAME, "nombre_conferencia").send_keys("Conferencia Innovación 2025")
    driver.find_element(By.NAME, "area_conocimiento").send_keys("Ciencias")
    driver.find_element(By.NAME, "fecha_envio").send_keys("2025-06-30")
    driver.find_element(By.NAME, "numero_revisores").send_keys("3")
    driver.find_element(By.NAME, "criterios_evaluacion").send_keys("Criterio 1, Criterio 2")
    driver.find_element(By.ID, "crear_conferencia").click()
    time.sleep(2)
    assert "El nombre de la conferencia ya está registrado" in driver.page_source

def test_create_conference_invalid_deadline():
    """
    Verifica que la creación de una conferencia falle si el deadline es inválido.

    Este escenario cubre el caso en el que el administrador intenta crear una conferencia 
    con una fecha de envío (deadline) menor a la fecha actual. El sistema debe mostrar un 
    mensaje de error indicando que la fecha es inválida.
    """
    login_as_admin()
    driver.get("http://127.0.0.1:8000/admin/conferencias")
    driver.find_element(By.LINK_TEXT, "Crear conferencia").click()
    driver.find_element(By.NAME, "nombre_conferencia").send_keys("Conferencia Innovación 2025")
    driver.find_element(By.NAME, "area_conocimiento").send_keys("Ciencias")
    driver.find_element(By.NAME, "fecha_envio").send_keys("2020-01-01")
    driver.find_element(By.NAME, "numero_revisores").send_keys("3")
    driver.find_element(By.NAME, "criterios_evaluacion").send_keys("Criterio 1, Criterio 2")
    driver.find_element(By.ID, "crear_conferencia").click()
    time.sleep(2)
    assert "La fecha debe ser mayor o igual a la actual" in driver.page_source

def close_browser():
    """
    Cierra el navegador después de realizar las pruebas.

    Este método cierra el navegador una vez que se han ejecutado todas las pruebas.
    """
    driver.quit()

# Ejecutar las pruebas
test_change_deadline_success()
test_change_deadline_failure()
test_update_conference_info_success()
test_update_conference_info_failure()
test_create_conference_success()
test_create_conference_name_duplicate()
test_create_conference_invalid_deadline()

close_browser()
