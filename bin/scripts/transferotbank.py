import requests
import simplejson as json

CONST_MRNONZ = "UX239I4NB1"
CONST_CESE   = "746H32ABMN"

def transferotbank(bank, from_Account, to_Account, Amount, from_Bank, to_Bank):

    if bank is '2':
        key = "CONST_MRNONZ"
        url = "http://bank.mrnonz.com/api/transfer"
    elif bank is '3':
        key = "CONST_CESE"
        url = 'http://glacial-gorge-51031.herokuapp.com/api/transfer'

    puredata = {}
    puredata['from_Account'] = from_Account
    puredata['to_Account'] = to_Account
    puredata['Amount'] = Amount
    puredata['from_Bank'] = from_Bank
    puredata['to_Bank'] = to_Bank
    puredata['key'] = key
    json_data = json.dumps(puredata)

    try:
        r = requests.post(url, json_data)
        response =  r.json()
    except Exception:
        response = {'status': False, 'error_message': 'Fail to connect server'}
    return response
