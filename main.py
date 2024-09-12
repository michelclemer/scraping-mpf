import os

from process_extractor import ProcessDataExtractor
from scraper import SeleniumScraper


def main():
    scraper = SeleniumScraper()

    try:
        process_number = os.getenv("PROCESS_NUMBER")

        raw_data = scraper.search_process(process_number)

        if raw_data:
            extractor = ProcessDataExtractor(raw_data)
            process_data = extractor.extract()
            print(process_data)
        else:
            print("Não foi possível encontrar os dados do processo.")

    finally:
        scraper.close()

if __name__ == "__main__":
    main()
