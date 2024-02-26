import re
from tabula import read_pdf
from ..models.ncmipi import NcmIpi
from adapters.db.ipi_operations import IpiOperations
from typing import List

class IpiUseCase:
    def __init__(self):
        self.ipi_operations = IpiOperations()

    def process_ipi(self):
        table_pdf = self.__get_table()
        full_ipi_list = []
        print("Starting PDF scraping..")
        for page in table_pdf:
            csv_rows = self.__page_to_csv(page)
            full_ipi_list.extend(self.__proccess_csv(csv_rows))
        print("Ended PDF scraping!")
        if len(full_ipi_list) > 0:
            self.ipi_operations.insert_ipi(full_ipi_list)

    
    def __get_table(self):
        pdf_file = "https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/legislacao/documentos-e-arquivos/tipi.pdf"
        #pdf_file = "tipi3.pdf"
        print(f"Gettings tables from file '{pdf_file}'...")
        table_pdf = read_pdf(
            pdf_file,
            pages="all",
            stream=True,
            encoding="utf-8"
        )
        print(f'Done getting tables from {pdf_file}!')
        return table_pdf
    
    def __page_to_csv(self, page) -> str:
        csv_string = page.to_csv(sep="^")
        return csv_string.split('\n')

    def __proccess_csv(self, csv_rows) -> List[NcmIpi]:
        if len(csv_rows) > 0 and "CÓDIGO DA TIPI" in csv_rows[0]:
            return []
        extracted_ipi_list = []
        for idx_row, row in enumerate(csv_rows):
            row_values = row.split('^')
            if (len(row_values) > 1 and row_values[1].count('.') == 2 and bool(re.search(r'\d{2}$', row_values[1]))):
                ncm, aliquota = row_values[1], row_values[len(row_values)-1]
                idx_ctrl = 1
                while True:
                    if (aliquota != "\r"):
                        break
                    next_row_values = csv_rows[idx_row+idx_ctrl].split("^")
                    aliquota = next_row_values[len(next_row_values)-1]
                    idx_ctrl += 1
                aliquota = self.__format_aliquota(aliquota) 
                extracted_ipi_list.append(NcmIpi(ncm, aliquota))
        return extracted_ipi_list

    def __format_aliquota(self, aliquota: str) -> float:
        aliquota = re.sub('[^0-9,]', "", aliquota).replace(",", ".")
        return 0.0 if aliquota == "" else float(aliquota)