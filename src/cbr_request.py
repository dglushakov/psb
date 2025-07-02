from doctest import debug

import requests
from bs4 import BeautifulSoup
import logging
import os

py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.DEBUG)
py_handler = logging.FileHandler(f"logs/{os.path.basename(__file__)}.log", mode='w', encoding='utf-8')
py_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)


# Crimea 2000000267269
# all 1315037839212
# Дальневосточный 1315038917989
def get_branch_info_by_id(internal_bank_id=1315037839212):
    url = "https://www.cbr.ru/FO_ZoomWS/FinOrg.asmx"
    result = []

    body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetBranchesInfoByID xmlns="http://web.cbr.ru/">
          <id>{internal_bank_id}</id>
          <page>0</page>
        </GetBranchesInfoByID>
      </soap:Body>
    </soap:Envelope>"""

    headers = {
        'content-type': 'text/xml; charset=utf-8',
        'Host': 'www.cbr.ru',
        'SOAPAction': 'http://web.cbr.ru/GetBranchesInfoByID',
        'Content-Length': str(len(body)),
    }

    py_logger.debug(f"Запрос дочерних подразделений по id = {internal_bank_id}")

    response = requests.post(url, data=body, headers=headers)
    py_logger.debug(f"Request status code = {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content.decode(), 'lxml')
        branch_records = soup.find_all('branchrecord')
        py_logger.debug(f"Получено {len(branch_records)} записей")
        py_logger.debug(branch_records)
        for branch_record in branch_records:
            py_logger.debug(f"Исходная запись: {branch_record}")
            new_office = {
                'internal_id': branch_record.find('id').text,
                'name': branch_record.find('name').text.lower(),
                'visible_name': branch_record.find('name').text,
                'address': branch_record.find('address').text.lower(),
                'visible_address': branch_record.find('address').text,
                'opendate': branch_record.find('opendate').text,
                'parent': branch_record.find('affiliation').text,
            }
            py_logger.debug(f'Добавляем офис в результирующую выборку : {new_office}')
            result.append(new_office)
            child_branches = None
            if branch_record.find('haschild').string == 'true':
                child_branches = get_branch_info_by_id(branch_record.find('id'))
            if child_branches is not None:
                py_logger.debug(f'extend = {child_branches}')
                result.extend(child_branches)
    else:
        print(f"Error : {response.status_code}")

    py_logger.debug(f"Результат {len(result)} офисов: {result}")
    py_logger.debug("Возвращаем результат")
    return result


if __name__ == "__main__":
    get_branch_info_by_id(2000000267269)
