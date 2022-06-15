import json
import base64
import os

import requests
import main
import get_bp_record
import accesstoken


class GetAttach:
    def __init__(self, access_token, path_dir):
        self.access_token = access_token
        self.path_dir = path_dir
        self.gb = get_bp_record.GetBp(self.access_token, self.path_dir)
        self.endpoint_url = "https://us2.unifier.oraclecloud.com/nyulangone/dev/ws/rest/service/v1/bp/record/file/"

    def get_input(self):
        self.bpname, self.record_no, self.project_number, self.input_params = self.gb.get_input()
        lineitem_file = input("Enter lineitem_file yes or no:")
        gen_com = input("Enter general_comments yes or no:")
        att_all = input("Enter attach_all_publication yes or no:")
        self.input_params = self.input_params + ", \"lineitem_file\": \"%s\", \"general_comments\": \"%ss\", \"attach_all_publications\": \"%s\""
        self.input_params = self.input_params % (lineitem_file, gen_com, att_all)
        print(self.input_params)
        # api-endpoint
        self.endpoint_url = self.endpoint_url + self.project_number + "?input={" + self.input_params + " }"
        # print(type(self.endpoint_url))
        # print(self.endpoint_url)
        return self.bpname, self.project_number

    def get_attach(self, out_path, out_file):
        # sending get request and saving the response as response object
        r = requests.get(url=self.endpoint_url,
                         headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        # extracting data in json format
        data = r.json()
        json_object = json.dumps(data, indent=4)
        json_dict_obj = json.loads(json_object)
        with open(os.path.join(self.path_dir, out_path, out_file), "w") as outfile:
            outfile.write(json_object)
        file_h = json_dict_obj['data'][0]['file_handler']
        # decoding the base64 encoded file_handler
        b64 = base64.b64decode(file_h)
        print(type(b64))
        # print(json_dict_obj['data'][0]['file_handler'])
        with open(os.path.join(self.path_dir, out_path, json_dict_obj['data'][0]['file_name']), "wb") as outfile:
            outfile.write(b64)


if __name__ == "__main__":
    file, path = main.file, main.path
    ac = accesstoken.AccessToken(file)
    a_token = ac.get_accesstoken()
    a = GetAttach(a_token, path)
    a.get_input()
    a.get_attach('out_files', "get_attach_record.json")
