class ProcessDataExtractor:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def extract(self):
        """Extrai as informações relevantes do dado bruto do processo."""
        if self.raw_data:
            return self.raw_data
        return None
