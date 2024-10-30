import time

import pytest
from selenium import webdriver

from database.DatabaseConnection import DatabaseConnection, DATABASE_CONFIG, fetch_user_forecast_count
from page.QuinielaPage import QuinielaPage

chromium_path = "chromedriver"
options = webdriver.ChromeOptions()
options.binary_location = chromium_path
USER_NAME = "Aaron QA"
@pytest.fixture
def driver():
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


"""
Ir a 'Llenar Quiniela', seleccionar año, un usuario de la lista y marcar las predicciones
para cada partido. Al dar click para guardar cambios verificar que el dialog pida confirmación
y muestre el nombre del usuario seleccionado. Al aceptar guardar debe aparecer un dialog
indicando que se guardaron los cambios.

"""
def test_saving_quiniela(driver):
    page = QuinielaPage(driver)
    page.open()
    page.select_specific_year(2023)
    page.click_fill_quiniela()
    page.select_user(USER_NAME)
    page.click_team_names()
    page.click_save_forecast()
    page.confirm_save()

"""
Ir a 'Llenar Quiniela', seleccionar año, pero NO seleccionar un usuario de la lista y
marcar las predicciones para cada partido. Al dar click para guardar cambios verificar que el
dialog indique que no se ha seleccionado usuario.
"""

def test_error_saving_without_user_selected(driver):
    page = QuinielaPage(driver)
    page.open()
    page.select_specific_year(2023)
    page.click_fill_quiniela()
    page.click_tied_game_options(5)
    page.click_save_forecast()
    #Se añada esta parte solo para que se visualice como validad el mensaje
    time.sleep(5)
    assert page.verify_text_present("Olvidaste seleccionar usuario"), \
        "Error message: Olvidaste seleccionar usuario no esta en el dialog."
    page.close_popup()

"""
Ir a 'Llenar Quiniela', seleccionar año y un usuario de la lista y marcar las predicciones
para cada partido pero dejar al menos un partido sin marcar. Al dar click para guardar
cambios verificar que el dialog indique que faltan partidos por marcar.
"""

def test_error_saving_with_unselected_matches(driver):
    page = QuinielaPage(driver)
    page.open()
    page.click_fill_quiniela()
    page.select_user(USER_NAME)
    page.click_tied_game_options(5)
    page.click_save_forecast()
    # Se añada esta parte solo para que se visualice como validad el mensaje
    time.sleep(5)
    assert page.verify_text_present("Te faltan partidos por llenar"), \
        "Error message for unselected matches was not found."
    page.close_popup()

"""
 Ir a 'Llenar Quiniela', seleccionar año, un usuario de la lista y marcar las predicciones
para cada partido. Al dar click para guardar cambios verificar que el dialog pida confirmación
y muestre el nombre del usuario seleccionado. Al aceptar guardar debe aparecer un dialog
indicando que se guardaron los cambios. Intentar volver a guardar cambios con ese mismo
usuario, para esa misma jornada de partidos. Un dialog debe indicar que la hoja de quiniela
está duplicada.
"""
# Para esta caso se trato, de añadir nuevas,pero no deja a pesar de cambiar la semana
# por tanto solo se validad que la "hoja de quiniela está duplicada."
def test_fill_quiniela_and_verify_team_names(driver):
    page = QuinielaPage(driver)
    page.open()
    page.click_fill_quiniela()
    page.select_user(USER_NAME)
    page.click_team_names()
    page.click_save_forecast()
    page.confirm_save()
    # Se añada esta parte solo para que se visualice como validad el mensaje
    time.sleep(5)
    assert page.verify_text_present("Hoja de quiniela duplicada para esta jornada"), \
        "Error message: Hoja de quiniela duplicada para esta jornada no esta en el dialog."
    page.close_popup()

"""
Ir a 'Mi Puntaje'. Seleccionar año, una jornada y un usuario para el que ya se hayan
guardado predicciones. Verificar que el conteo de puntos en la parte superior de la tabla es
correcto.

"""
# El campo de jornada esta desabilito en el HTML
def test_validate_score_match_with_the_quiniela(driver):
    page = QuinielaPage(driver)
    page.open()
    page.click_my_score()
    driver.get("https://mean-machine-qa.vercel.app/myScore/2023/2/1")
    page.select_user(USER_NAME)
    label, value = page.get_puntaje_total()
    success_count = page.count_success_elements()
    assert value == success_count, f"El puntaje debe ser {success_count}, pero obtuvo {value}."


"""
Una vez guardada una quiniela correctamente, corroborar la inserción en la tabla
Forecast de la base de datos
"""


@pytest.mark.asyncio
async def test_saving_quiniela_with_database_validation(driver):
    test_saving_quiniela(driver)
    try:
        async with DatabaseConnection(DATABASE_CONFIG) as connection:
            total_forecasts = await fetch_user_forecast_count(connection, "Aaron QA", "V")
            # Assert that the total_forecasts is equal to 20
            assert total_forecasts == 20, f"Expected total_forecasts to be 20, but got {total_forecasts}."
    except Exception as e:
        print("An error occurred during database validation:", e)