import requests
from bs4 import BeautifulSoup


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

    response = requests.post(url, data=body, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content.decode(), 'lxml')
        for branch_record in soup.find_all('branchrecord'):
            new_office = {
                'internal_id': branch_record.find('id').text,
                'name': branch_record.find('name').text.lower(),
                'visible_name': branch_record.find('name').text,
                'address': branch_record.find('address').text.lower(),
                'visible_address': branch_record.find('address').text,
                'opendate': branch_record.find('opendate').text,
                'parent': branch_record.find('affiliation').text,
            }
            print('append :', new_office)
            result.append(new_office)
            child_branches = None
            if branch_record.find('haschild').string == 'true':
                print('requesting child branches for id ', branch_record.find('id'), branch_record.find('name'))
                child_branches = get_branch_info_by_id(branch_record.find('id'))
            if child_branches is not None:
                print('extend ', child_branches)
                result.extend(child_branches)
    else:
        print(f"Error : {response.status_code}")

    return result
