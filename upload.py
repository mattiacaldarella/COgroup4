"""
This script uploads all our solutions for the list of file names specified in the main method
"""

import requests
from config import SOLUTIONS_DIR
import os
import json
import time

# INSTANCE_IDS = {'challenge_r100d10_1.txt': '1-c2d66c53a4bd89bddc9e619085a3e70d.txt', 'challenge_r100d10_2.txt': '1-e732a27c9ad03c1b42bed54b94ed5341.txt', 'challenge_r100d10_3.txt': '1-3ac1fb1ef9a1504edd26e920b37fbe80.txt', 'challenge_r100d10_4.txt': '1-55aa69effd0f7616859534716347def9.txt', 'challenge_r100d10_5.txt': '1-cb30cca0465671fbd3e28c1aa4886db7.txt', 'challenge_r200d15_1.txt': '1-96b13962beaeacb72029444472773d22.txt', 'challenge_r200d15_2.txt': '1-4a3044a978eb19f9ce5346590a3ffe74.txt', 'challenge_r200d15_3.txt': '1-99d2ffedb8c19de2bd65d20c16770a8a.txt', 'challenge_r200d15_4.txt': '1-a53096921da8c84a4b8da27b8440ef2c.txt', 'challenge_r200d15_5.txt': '1-90b7dd95deac77a55e980689cf1270f6.txt', 'challenge_r300d20_1.txt': '1-3a0663e7d01445f8c5c1f8d561611bc8.txt', 'challenge_r300d20_2.txt': '1-6dd2e162cc64c1533b7de1305d72a60d.txt', 'challenge_r300d20_3.txt': '1-d1056f3e35575c1580f4d6100903cfc9.txt', 'challenge_r300d20_4.txt': '1-26a96612d88de95b80457f000799664f.txt', 'challenge_r300d20_5.txt': '1-8337fb8767bc4c827b1459969b6c02cd.txt', 'challenge_r500d25_1.txt': '1-a5bd0f13cf2e9e6a232340c6e9046217.txt', 'challenge_r500d25_2.txt': '1-9839896a071c39df4961476452d43879.txt', 'challenge_r500d25_3.txt': '1-5ce82ed2d6bc46fb058ed317dd58133f.txt', 'challenge_r500d25_4.txt': '1-0e03130b8e5010a99e9f66075b4bdfaa.txt', 'challenge_r500d25_5.txt': '1-a4303ab17eb69e118f9da775e887b15d.txt'}
INSTANCE_REFS = {'challenge_r100d10_1.txt': '{ "categoryId": "1", "instanceId": "1-c2d66c53a4bd89bddc9e619085a3e70d.txt" }', 'challenge_r100d10_2.txt': '{ "categoryId": "1", "instanceId": "1-e732a27c9ad03c1b42bed54b94ed5341.txt" }', 'challenge_r100d10_3.txt': '{ "categoryId": "1", "instanceId": "1-3ac1fb1ef9a1504edd26e920b37fbe80.txt" }', 'challenge_r100d10_4.txt': '{ "categoryId": "1", "instanceId": "1-55aa69effd0f7616859534716347def9.txt" }', 'challenge_r100d10_5.txt': '{ "categoryId": "1", "instanceId": "1-cb30cca0465671fbd3e28c1aa4886db7.txt" }', 'challenge_r200d15_1.txt': '{ "categoryId": "1", "instanceId": "1-96b13962beaeacb72029444472773d22.txt" }', 'challenge_r200d15_2.txt': '{ "categoryId": "1", "instanceId": "1-4a3044a978eb19f9ce5346590a3ffe74.txt" }', 'challenge_r200d15_3.txt': '{ "categoryId": "1", "instanceId": "1-99d2ffedb8c19de2bd65d20c16770a8a.txt" }', 'challenge_r200d15_4.txt': '{ "categoryId": "1", "instanceId": "1-a53096921da8c84a4b8da27b8440ef2c.txt" }', 'challenge_r200d15_5.txt': '{ "categoryId": "1", "instanceId": "1-90b7dd95deac77a55e980689cf1270f6.txt" }', 'challenge_r300d20_1.txt': '{ "categoryId": "1", "instanceId": "1-3a0663e7d01445f8c5c1f8d561611bc8.txt" }', 'challenge_r300d20_2.txt': '{ "categoryId": "1", "instanceId": "1-6dd2e162cc64c1533b7de1305d72a60d.txt" }', 'challenge_r300d20_3.txt': '{ "categoryId": "1", "instanceId": "1-d1056f3e35575c1580f4d6100903cfc9.txt" }', 'challenge_r300d20_4.txt': '{ "categoryId": "1", "instanceId": "1-26a96612d88de95b80457f000799664f.txt" }', 'challenge_r300d20_5.txt': '{ "categoryId": "1", "instanceId": "1-8337fb8767bc4c827b1459969b6c02cd.txt" }', 'challenge_r500d25_1.txt': '{ "categoryId": "1", "instanceId": "1-a5bd0f13cf2e9e6a232340c6e9046217.txt" }', 'challenge_r500d25_2.txt': '{ "categoryId": "1", "instanceId": "1-9839896a071c39df4961476452d43879.txt" }', 'challenge_r500d25_3.txt': '{ "categoryId": "1", "instanceId": "1-5ce82ed2d6bc46fb058ed317dd58133f.txt" }', 'challenge_r500d25_4.txt': '{ "categoryId": "1", "instanceId": "1-0e03130b8e5010a99e9f66075b4bdfaa.txt" }', 'challenge_r500d25_5.txt': '{ "categoryId": "1", "instanceId": "1-a4303ab17eb69e118f9da775e887b15d.txt" }'}

def upload_solution_from_path(file_name):
    cookies = {
        "ARRAffinity": "52a38c849f396c288b326df960005ec1abc48170f4e3f0d3ccd01f27572cdeb7",
        "ARRAffinitySameSite": "52a38c849f396c288b326df960005ec1abc48170f4e3f0d3ccd01f27572cdeb7",
        "connect.sid": "s%3AV2E50g13EQ2O20J9x-iXJvsks6ye0FFG.6GnbiU8xDlNE6Hog8dmcdnYDJbYx35s8pTXbgyZTLpk",
    }

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryEXQFoJL1fd74A4zB",
        # 'Cookie': 'ARRAffinity=52a38c849f396c288b326df960005ec1abc48170f4e3f0d3ccd01f27572cdeb7; ARRAffinitySameSite=52a38c849f396c288b326df960005ec1abc48170f4e3f0d3ccd01f27572cdeb7; connect.sid=s%3AV2E50g13EQ2O20J9x-iXJvsks6ye0FFG.6GnbiU8xDlNE6Hog8dmcdnYDJbYx35s8pTXbgyZTLpk',
        "Origin": "https://co2020-ba-vu.challenges.ortec.com",
        "Referer": "https://co2020-ba-vu.challenges.ortec.com/upload-solution",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
    }


    files = {
        "instanceReference": (None, INSTANCE_REFS[file_name]),
        "solution": (file_name, open(os.path.join(f"{SOLUTIONS_DIR}", file_name), "rb"), "text/plain")
    }

    response = requests.post(
        "https://co2020-ba-vu.challenges.ortec.com/upload-solution",
        cookies=cookies,
        headers=headers,
        files=files,
    )

    # print(response.request.body.decode())
    print(response.content.decode())

if __name__ == "__main__":
    for file_name in ['challenge_r100d10_5.txt', 'challenge_r500d25_1.txt', 'challenge_r300d20_5.txt', 'challenge_r100d10_4.txt', 'challenge_r500d25_3.txt', 'challenge_r200d15_2.txt', 'challenge_r100d10_3.txt', 'challenge_r300d20_1.txt', 'challenge_r300d20_2.txt', 'challenge_r200d15_3.txt', 'challenge_r500d25_5.txt', 'challenge_r200d15_1.txt', 'challenge_r300d20_4.txt', 'challenge_r200d15_5.txt', 'challenge_r500d25_4.txt', 'challenge_r500d25_2.txt', 'challenge_r100d10_2.txt', 'challenge_r300d20_3.txt', 'challenge_r100d10_1.txt']:
        print(f"Uploading {file_name}:")
        time.sleep(.5)
        upload_solution_from_path(file_name)
