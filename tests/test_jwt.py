
# Import the "requests" python module:
import requests
import jwt
import datetime
import logging
verify_ssl = False
logging.captureWarnings(True)



# Save the copied credentials.json from the website into a variable "key":
key = {
  "api_key": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZlbmNlX2tleV8yMDE4LTEyLTAzVDE5OjAxOjA4WiJ9.eyJhenAiOiIiLCJqdGkiOiJjMTVhYTY4Yi0wMjJkLTRjYmUtOGZmYi05MGFmODUwMTNjOGMiLCJhdWQiOlsiZGF0YSIsInVzZXIiLCJmZW5jZSIsIm9wZW5pZCJdLCJleHAiOjE1NDY0NTY1OTcsImlzcyI6Imh0dHBzOi8vbG9jYWxob3N0L3VzZXIiLCJpYXQiOjE1NDM4NjQ1OTcsInB1ciI6ImFwaV9rZXkiLCJzdWIiOiIxIn0.C_PEQ3DlcoVFEBlXgOo5MXGXnN_J95oMOpTSPJMA91noXDoLxEuzFn0CdBonBhtuKjIdOhDVDTd8mat_-6_poeiuW-iUAfDCouMPtmg9Z3ikJt_AtL_bqfy-yOGZr9I9DWHpZbq1Hk3WVY08U-GnhZTvAXMgWwIMknxg30qvPs03goyP1F3SXl44_R9MA_O1x2OYMo_idEynFkBiNFFRUmaqcN3NG9TNvVSfi3LHkRRx5y71pd4CnKs2NFqKm_mK_Z63QyeGVGI8n6NvecyBqNovuSzL9nt8kCmypeltqdkpez_o-kyFEfK_vAm8MsEaAciN9O0qJjs13XWhMTHFMw",
  "key_id": "c15aa68b-022d-4cbe-8ffb-90af85013c8c"
}
TOKEN = {u'access_token': u'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZlbmNlX2tleV8yMDE4LTEyLTAzVDE5OjAxOjA4WiJ9.eyJjb250ZXh0Ijp7InVzZXIiOnsicG9saWNpZXMiOltdLCJnb29nbGUiOnsicHJveHlfZ3JvdXAiOm51bGx9LCJpc19hZG1pbiI6dHJ1ZSwibmFtZSI6ImJyaWFuQGJ3YWxzaC5jb20iLCJwcm9qZWN0cyI6eyJ0ZXN0IjpbInJlYWQiLCJjcmVhdGUiLCJ1cGxvYWQiLCJ1cGRhdGUiLCJkZWxldGUiXX19fSwianRpIjoiMWEyZDQwMDctYWE0ZS00NjU1LTk3YTUtY2M5NDRhOGQ0YjNiIiwiYXVkIjpbImRhdGEiLCJ1c2VyIiwiZmVuY2UiLCJvcGVuaWQiXSwiZXhwIjoxNTQ0MDU4NjI3LCJhenAiOiIiLCJpc3MiOiJodHRwczovL2xvY2FsaG9zdC91c2VyIiwiaWF0IjoxNTQ0MDU1MDI3LCJwdXIiOiJhY2Nlc3MiLCJzdWIiOiIxIn0.pa2vvmfsVFsrcd1qNV_L9giRDhjG0SgWR_UktuvvpDpxmlbyqYUsKHzehJAAMo7ZBWFUC_2MDLXRCV5juDVQ1RRShjT7mTYo8vp6cEhPh5R7lIyYWH_HpCjxfntTx9UHUQ9zSb-SAE_tqFG2iLey8uZQJvb-Nq0MLVPQrQqoHLxxenv69phBIF91E5N2sCk4FunF7gtRrCFI0EOJadkZzgjI3OfV0_w6CRZ7LVtbYNimG6RXBYHsiUpZwzeth8IGN57kSVczTnHOxNyA64Et60MMeOYQnmMf46exq_XY-DMxIFEd2kA2JSiJDawzMv6GuTLA-m7Siz5r-e-fZf5vbA'}


def _decode_access_token(token):
    return jwt.decode(
        token['access_token'],
        options = {'verify_exp': True, 'verify_signature': False, 'verify_aud': False, }
    )

def test_jwt_access():
    # verify access token still OK
    decoded_access_token = None
    token = TOKEN
    try:
        decoded_access_token = _decode_access_token(token)
    except Exception as e:
        print(e)
        print('refreshing access token')
        token = requests.post('https://localhost/user/credentials/cdis/access_token',
            json=key, verify=verify_ssl).json()
        decoded_access_token = _decode_access_token(token)
        exp = datetime.datetime.fromtimestamp(decoded_access_token['exp']).strftime('%Y-%m-%d %H:%M:%S')
        print('new token expires = {}'.format(exp))




    # test valid & invalid token
    headers = {'Authorization': 'bearer {}'.format(token['access_token'])}
    invalid_headers = {'Authorization': 'bearer DUMMY_{}'.format(token['access_token'])}
    # # Test indexd endpoint
    # index = requests.get('https://localhost/index/ed6f1b44-f40c-4e9c-8a8d-86aa2a93896f', headers=headers, verify=verify_ssl)
    # assert index.status_code == 200, 'object should be readable with valid token'
    #
    # index = requests.get('https://localhost/index/ed6f1b44-f40c-4e9c-8a8d-86aa2a93896f', headers=invalid_headers, verify=verify_ssl)
    # assert index.status_code == 500, 'object should not be readable with invalid token'
    #
    # # Test GraphQL Endpoint Query
    # query = {'query':"""{ project { id, type, code } }"""};
    # project = requests.post('https://localhost/api/v0/submission/graphql/', json=query, headers=headers, verify=verify_ssl)
    # assert project.status_code == 200
    #
    # project = requests.post('https://localhost/api/v0/submission/graphql/', json=query, headers=invalid_headers, verify=verify_ssl)
    # assert project.status_code == 500


    # case = { "type": "case", "experiments": [ { "submitter_id": "test" } ], "submitter_id": "case3" }
    # case = requests.put(' https://localhost/api/v0/submission/test/test/', json=case, headers=headers, verify=verify_ssl)
    # assert case.status_code == 200

    case = { "type": "case", "experiments": [ { "submitter_id": "test" } ], "submitter_id": "case4" }
    case = requests.put(' https://localhost/api/v0/submission/test/test/', json=case, headers=invalid_headers, verify=verify_ssl)
    assert case.status_code == 500
