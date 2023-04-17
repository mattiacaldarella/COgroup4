"""
I used this to parse out the instanceRefs from the javascript. Not needed anymore
"""

import json

option_data = """          <option
            value='{ "categoryId": "1", "instanceId": "1-c2d66c53a4bd89bddc9e619085a3e70d.txt" }'
          >
            challenge_r100d10_1.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-e732a27c9ad03c1b42bed54b94ed5341.txt" }'
          >
            challenge_r100d10_2.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-3ac1fb1ef9a1504edd26e920b37fbe80.txt" }'
          >
            challenge_r100d10_3.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-55aa69effd0f7616859534716347def9.txt" }'
          >
            challenge_r100d10_4.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-cb30cca0465671fbd3e28c1aa4886db7.txt" }'
          >
            challenge_r100d10_5.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-96b13962beaeacb72029444472773d22.txt" }'
          >
            challenge_r200d15_1.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-4a3044a978eb19f9ce5346590a3ffe74.txt" }'
          >
            challenge_r200d15_2.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-99d2ffedb8c19de2bd65d20c16770a8a.txt" }'
          >
            challenge_r200d15_3.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-a53096921da8c84a4b8da27b8440ef2c.txt" }'
          >
            challenge_r200d15_4.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-90b7dd95deac77a55e980689cf1270f6.txt" }'
          >
            challenge_r200d15_5.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-3a0663e7d01445f8c5c1f8d561611bc8.txt" }'
          >
            challenge_r300d20_1.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-6dd2e162cc64c1533b7de1305d72a60d.txt" }'
          >
            challenge_r300d20_2.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-d1056f3e35575c1580f4d6100903cfc9.txt" }'
          >
            challenge_r300d20_3.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-26a96612d88de95b80457f000799664f.txt" }'
          >
            challenge_r300d20_4.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-8337fb8767bc4c827b1459969b6c02cd.txt" }'
          >
            challenge_r300d20_5.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-a5bd0f13cf2e9e6a232340c6e9046217.txt" }'
          >
            challenge_r500d25_1.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-9839896a071c39df4961476452d43879.txt" }'
          >
            challenge_r500d25_2.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-5ce82ed2d6bc46fb058ed317dd58133f.txt" }'
          >
            challenge_r500d25_3.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-0e03130b8e5010a99e9f66075b4bdfaa.txt" }'
          >
            challenge_r500d25_4.txt
          </option>

          <option
            value='{ "categoryId": "1", "instanceId": "1-a4303ab17eb69e118f9da775e887b15d.txt" }'
          >
            challenge_r500d25_5.txt
          </option>"""

instance_refs = {}
for line in option_data.split("\n"):
    if "value" in line:
        # instance_id = line.split('"instanceId": "')[1].split('"')[0]
        instance_ref = line.split("value='")[1].split("'")[0]
        # print(instance_id)
    elif ".txt" in line:
        file_name = line.strip()
        instance_refs[file_name] = instance_ref

print(instance_refs)