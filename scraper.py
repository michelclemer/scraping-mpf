import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from config import Config


class SeleniumScraper:
    def __init__(self):
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """Inicializa o WebDriver sem precisar de um driver local."""
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(Config.BASE_URL)
        return driver

    def _get_first_link(self):
        WebDriverWait(self.driver, Config.TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "panel-heading"))
        )
        time.sleep(2)
        first_link = self.driver.execute_script("""
            let x = document.getElementsByClassName('panel-heading');
            let y = Array.from(x);
            let divs = y.filter((e) => e.id && e.id.includes('div'));
            return divs[0].children[1].href;
        """)
        return first_link

    def search_process(self, process_number: str):
        """Consulta um processo no site do MPF."""
        self._enter_process_number(process_number)
        self._submit_search()
        self._select_process()
        return self._extract_process_data()

    def _enter_process_number(self, process_number: str):
        """Entra com o número do processo no campo apropriado."""
        input_field = WebDriverWait(self.driver, Config.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="q"]'))
        )
        input_field.clear()
        input_field.send_keys(process_number)

    def _submit_search(self):
        """Submete a pesquisa do processo."""
        search_button = self.driver.find_element(By.ID, "btnPesquisar")
        search_button.click()

    def _select_process(self):
        """Seleciona o processo na página de resultados."""
        link = self._get_first_link()
        self.driver.get(link)

    def _extract_process_data(self):
        """Extrai os dados do processo da página de resultados."""
        try:
            result_element = WebDriverWait(self.driver, Config.TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "tab_proc"))
            )
            process_data = {
                'tombo': result_element.find_element(By.XPATH, '//*[@id="tab_proc"]/tbody/tr[1]/td[3]/div[1]/span').text,
                'NUP': result_element.find_element(By.XPATH, '//*[@id="tab_proc"]/tbody/tr[2]/td[2]/div').text,
                'Advogado': result_element.find_element(By.XPATH, '//*[@id="tab_proc"]/tbody/tr[11]/td[2]/div').text,
                'Grupo Temático': result_element.find_element(By.XPATH, '//*[@id="tab_proc"]/tbody/tr[12]/td[2]/div').text,
            }
        except Exception as e:
            process_data = None
            print(f"Erro ao extrair dados do processo: {e}")

        return process_data

    def close(self):
        """Fecha o WebDriver."""
        self.driver.quit()
