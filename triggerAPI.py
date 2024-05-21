#!/bin/python3

import os
import datetime
import time
import io
import json
import requests
import sys
import yaml

def get_authToken():
    headers = {'Content-type': 'application/json'}
    data = {'applicationID': 'app_BankofAmericaJakarta_Payments_SB', 
            'authn': {
                'client_id': 'CASHPRO_Y5FG0DLJ_051624051315_SB',
                'client_secret': 'uQENgkrmEh6w0fbBEEtG97UhorUlQjF2uKCLoY468DZ0C9oAHrPeKKU3qn0h1CEH'
                }
            }

    response = requests.post(f"https://api-sb.bofa.com/authn/v1/client-authentication", data=json.dumps(data), headers=headers)
    
    print(f"==========================================================================")
    print(f"Generating Access Token")
    print(f"==========================================================================")
    print(f"Request Header: {response.request.headers}")
    print(f"Request Body: {response.request.body}")
    print(f"Request Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"==========================================================================")

    if response.status_code != 200:
        print(f"Failed to get Acces Token.")
        print(f"==========================================================================")
        return False
    
    return response.json()

def sendBIFAST():
    uniqueKey = round(time.time() * 1000)
    reqestedExecutionDate = datetime.datetime.now()
    access_token = get_authToken()
    if not access_token:
        return
    
    if access_token['access_token'] is None:
        return
    
    headers = {
        'Content-type': 'application/json',
        'Authorization': f"{access_token['token_type']} {access_token['access_token']}",
        'X-Idempotency-Key': f'XIDEM-{uniqueKey}'
    }

    data = {
        'paymentIdentification': {
            'instructionIdentification': f"INS-{uniqueKey}",
            'endToEndIdentification': f"E2EID-{uniqueKey}"
        },
        "paymentMethod": 'TRF',
        'requestedExecutionDate': datetime.datetime.now().strftime('%Y-%m-%d'),
        'amount': {
            'value': '10000.00'
        },
        'debtor': {
            'name': 'Lutfi Widayanto',
            'identifier': [
                {
                    'identification': '1234567890',
                    'schemeName': 'BANA Jakarta'
                }
            ]
        },
        'debtorAccount': {
            'identification': '1234567890',
            'currency': 'IDR'
        },
        'debtorAgent': {
            'institution': {
                'name': "Bank of America, Jakarta",
                'identification': 'BOFAID2X',
                'postalAddress': {
                    'country': 'ID'
                }
            }
        },
        'creditor': {
            'name': 'Creditor Name',
            'postalAddress':{
                'addressLine':[
                    'Creditor Address 1',
                    'Creditor Address 2'
                ],
                'postalCode': '12345',
                'city': 'Jakarta',
                'countrySubDivision': 'Jakarta',
                'country': 'ID'
            }
        },
        'creditorAccount': {
            'identification': '1234567890',
            'currency': 'IDR'
        },
        'creditorAgent':{
            'institution':{
                'identification': 'CENAIDJA',
                'postalAddress': {
                    'country': 'ID'
                }
            }
        },
        'paymentType': {
            'serviceLevel': 'SDVA',
            'localInstrument': 'CCD',
            'categoryOfPurpose': '99'
        },
        'unstructuredRemittance': 'Testing'
    }

    response = requests.post(f"https://api-sb.bofa.com/cashpro/payments/v2/payment-initiations", data=json.dumps(data), headers=headers)

    print(f"Initiating Payment Request")
    print(f"==========================================================================")
    print(f"Request Header: {response.request.headers}")
    print(f"Request Body: {response.request.body}")
    print(f"Request Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"==========================================================================")


if __name__ == '__main__':
    sendBIFAST()