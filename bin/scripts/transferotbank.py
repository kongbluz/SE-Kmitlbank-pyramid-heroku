import requests
import simplejson as json

CONST_MRNONZ = "kong2222"
CONST_CESE   = "4R02vZ4c69"

def transferotbank(bank, from_Account, to_Account, Amount):

    if bank is '2':
        key = CONST_MRNONZ
        url = "http://bank.route.in.th:9999/api/transfer"
    elif bank is '3':
        key = CONST_CESE
        url = 'http://161.246.70.75:8080/cesebank/api/Transferapi.php'

    puredata = {}
    puredata['from_Account'] = from_Account
    puredata['to_Account'] = to_Account
    puredata['Amount'] = Amount
    puredata['key'] = key
    json_data = json.dumps(puredata)

    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json_data, headers=headers)
        response =  r.json()
    except Exception:
        response = {'status': False, 'error_message': 'Fail to connect server'}
    return response
