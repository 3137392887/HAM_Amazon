from config import LOG_PATH, LIMITE_PRODUCTOS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os
import re


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def iniciar_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    time.sleep(3)
    return driver

def buscar_productos_amazon(producto, driver, limite=LIMITE_PRODUCTOS):
    logging.info(f"Iniciando búsqueda para: {producto}")
    resultados = []
    pagina = 1

    try:
        driver.get("https://www.amazon.com/-/es/?currency=USD")
        time.sleep(2)
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))

        barra_busqueda = driver.find_element(By.ID, "twotabsearchtextbox")
        barra_busqueda.clear()
        barra_busqueda.send_keys(producto)
        barra_busqueda.send_keys(Keys.RETURN)

        while len(resultados) < limite:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))
            time.sleep(3)

            items = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")

            for item in items:
                if len(resultados) >= limite:
                    break

                try:
                    nombre = item.find_element(By.CSS_SELECTOR, "a > h2 > span").text
                except Exception:
                    nombre = "No disponible"

                precio = None
                try:
                    precio_entero = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                    precio_decimal = item.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                    precio_texto = precio_entero.replace(",", "") + "." + precio_decimal
                    precio = float(precio_texto) if precio_texto.replace(".", "").isdigit() else None
                    logging.debug(f"Precio obtenido por formato estándar: {precio}")
                except Exception:
                    try:
                        elementos_base = item.find_elements(By.CSS_SELECTOR, "span.a-color-base")
                        texto_base = ""
                        if len(elementos_base) >= 2:
                            texto_base = elementos_base[1].text
                        elif elementos_base:
                            texto_base = elementos_base[0].text

                        match = re.search(r"\$?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", texto_base)
                        if match:
                            precio_texto = match.group(1).replace(",", "")
                            precio = float(precio_texto)
                        logging.debug(f"Precio obtenido por texto plano: {precio}")
                    except Exception as e:
                        logging.debug(f"No se pudo obtener precio: {e}")

                entrega = "No disponible"
                for selector in [
                    ".a-row.a-color-base.udm-primary-delivery-message",
                    ".a-row.a-size-base.a-color-secondary"
                ]:
                    try:
                        elemento = item.find_element(By.CSS_SELECTOR, selector)
                        texto = elemento.text.strip()
                        if texto:
                            entrega = texto
                            break
                    except:
                        continue

                if nombre != "No disponible" and precio is not None:
                    resultados.append({
                        "nombre": nombre,
                        "precio_usd": precio,
                        "entrega": entrega
                    })
                    logging.info(f"Producto agregado: {nombre} - ${precio}")
                else:
                    logging.warning(f"Producto descartado por datos incompletos: nombre='{nombre}', precio='{precio}'")

            # Avanzar a la siguiente página
            try:
                siguiente = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
                driver.execute_script("arguments[0].scrollIntoView();", siguiente)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", siguiente)  
                pagina += 1
                logging.info(f"Avanzando a la página {pagina}")
            except Exception as e:
                logging.warning(f"No se pudo avanzar a la página {pagina}: {e}")
                break


        logging.info(f"Total de productos encontrados: {len(resultados)}")
        return resultados

    except Exception as e:
        logging.error(f"Error al buscar {producto}: {e}")
        return []