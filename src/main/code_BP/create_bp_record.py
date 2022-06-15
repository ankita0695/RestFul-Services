import requests
import accesstoken
import main
import json
import os
import get_bp_record


class CreateBp:
    def __init__(self, access_token, path_dir):
        self.data = None
        self.access_token = access_token
        self.path_dir = path_dir
        self.gb = get_bp_record.GetBp(self.access_token, self.path_dir)

    def get_bp_record(self):
        self.bpname, self.record_no, self.project_number, self.input_params = self.gb.get_input()
        self.endpoint_url = "https://us2.unifier.oraclecloud.com/nyulangone/dev/ws/rest/service/v1/bp/record/" + self.project_number
        self.gb.get_bp('in_files', 'get_record.json')

    def get_data(self):
        with open(os.path.join(self.path_dir, 'in_files', 'get_record.json'), 'r') as jfile:
            data = json.load(jfile)
        # inter_data = dict()
        data["data"][0].pop("record_no")
        data.pop("message")
        data.pop("status")
        # data["data"][0].pop("nyu_si_project_type")
        data["data"][0]["inv_invoice_num1"] = data["data"][0]["inv_invoice_num1"] + "_t"
        # data["data"][0]["nyu_ps_po_id"] = data["data"][0]["nyu_ps_po_id"] + "-test"
        # print(data["data"][0]["inv_invoice_num1"])
        data["options"] = dict()
        data["options"]["bpname"] = self.bpname
        # inter_data["data"] = data["data"]
        self.data = data
        # json_object = json.dumps(self.data, indent=4)
        # with open(os.path.join(self.path_dir, 'in_files', "get_inter_record.json"), "w") as outfile:
        #     outfile.write(json_object)

    def create_bp(self):
        # sending post request and saving response as response object
        r = requests.post(url=self.endpoint_url, json=self.data,
                          headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        # extracting response text
        # print(r)
        records_test = r.json()
        # print(type(records_test))
        record_status = dict()
        record_status["record_status"] = records_test["message"][0]["_record_status"]
        record_status["status"] = records_test["status"]
        json_object = json.dumps(record_status, indent=4)
        with open(os.path.join(self.path_dir, 'out_files', "create_record.json"), "w") as outfile:
            outfile.write(json_object)


if __name__ == "__main__":
    file, path= main.file, main.path
    a = accesstoken.AccessToken(file)
    a_token = a.get_accesstoken()
    c = CreateBp(a_token, path)
    c.get_bp_record()
    c.get_data()
    # c.create_bp()
