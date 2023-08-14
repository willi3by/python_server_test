import requests
import pydicom
from pathlib import Path
from urllib3.filepost import encode_multipart_formdata, choose_boundary

from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

dicom_service_name = "brainkeydicom"
service_url = "https://thebrainkeydicomspace-brainkeydicom.dicom.azurehealthcareapis.com"
base_url = f"{service_url}/v1"

def encode_multipart_related(fields, boundary=None):
    if boundary is None:
        boundary = choose_boundary()

    body, _ = encode_multipart_formdata(fields, boundary)
    content_type = str('multipart/related; boundary=%s' % boundary)

    return body, content_type

def get_bearer_token(credential_type = 3):
    # Credential type depends on your system. Azure CLI for Mac is type 3, Powershell for windows is type 4.
    token = credential.credentials[3].get_token('https://dicom.healthcareapis.azure.com')
    bearer_token = f'Bearer {token.token}'
    return bearer_token

def get_changefeed(bearer_token):
    client = requests.session()
    bearer_token = get_bearer_token()
    headers = {"Authorization":bearer_token}
    url= f'{base_url}/changefeed'

    response = client.get(url,headers=headers)
    if (response.status_code != 200):
        print('Error! Likely not authenticated!')
    return response

def post_dicom(dicom, isFile = False, filepath = None):
    if isFile:
        with open(filepath, "rb") as reader:
            rawfile = reader.read()
    else:
        rawfile = dicom
    
    client = requests.session()
    files = {"file": ("dicomfile", rawfile, "application/dicom")}
    body, content_type = encode_multipart_related(fields = files)
    
    bearer_token = get_bearer_token()
    
    headers = {'Accept':'application/dicom+json', 
               "Content-Type":content_type, 
               "Authorization":bearer_token}
    
    url = f'{base_url}/studies'
    response = client.post(url, body, headers=headers, verify=False)
    return response
    
    