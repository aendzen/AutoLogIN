import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import configparser

# Funktion, um das Skript auszuführen
def run_script():
    # Konfigurationsdatei
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Login-Daten und WebDriver-Pfad aus der Konfigurationsdatei
    username = config['LOGIN']['username']
    password = config['LOGIN']['password']
    webdriver_path = config['SETTINGS']['webdriver_path']

    # Optionen für den WebDriver
    firefox_options = Options()
    firefox_options.add_argument("--start-maximized")

    # WebDriver initialisieren
    service = Service(webdriver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # Seite aufrufen
    driver.get('https://portal.cc-student.com/index.php?cmd=kug')

    # Warte, bis die Seite vollständig geladen ist
    time.sleep(3)

    # Benutzername und Passwort sind nicht direkt in der Datei, sondern werden aus einer externen Datei abgerufen
    username_field = driver.find_element(By.NAME, 'login_username')  
    password_field = driver.find_element(By.NAME, 'login_passwort')  

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Finde und klicke auf den Login-Button, urspünglich wollte ich auch hier die ID ansprechen, war aber nicht möglich
    login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Einloggen']")
    login_button.click()

    # Warte, um sicherzustellen, dass das Einloggen abgeschlossen ist
    time.sleep(5)

    # Finde den Button "Zeiterfassung" und klicke darauf, hier musste ich einen anderen Weg finden um den Button zu identifizieren, da sich die ID immer wieder ändert
    zeiterfassung_button = driver.find_element(By.NAME, "showDialogButton")
    zeiterfassung_button.click()

    # Warte, um sicherzustellen, dass die Aktion abgeschlossen ist
    time.sleep(5)

    # Finde den Button "Kommen/Gehen" und klicke darauf, die selbe Problematik gab es auch wieder bei diesem Button
    kommengehen_button = driver.find_element(By.NAME, "kommengehenbutton")
    kommengehen_button.click()

    # Warte, um sicherzustellen, dass die Aktion abgeschlossen ist
    time.sleep(5)

    # Browser schließen
    driver.quit()

# Zeitplanung für das Skript
schedule.every().day.at("14:00").do(run_script)  # Uhrzeit Einloggen
schedule.every().day.at("22:00").do(run_script)  # Uhrzeit Ausloggen

# Endlose Schleife, die die geplanten Aufgaben ausführt
while True:
    schedule.run_pending()
    time.sleep(1)
