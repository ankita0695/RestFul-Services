import json
import os
import requests
import main
import get_bp_attach
import accesstoken


class CreateAttach:
    def __init__(self, access_token, path):
        self.project_number = None
        self.bpname = None
        self.data = None
        self.accesstoken = access_token
        self.path_dir = path
        self.endpoint_url = "https://us2.unifier.oraclecloud.com/nyulangone/" + main.env + "/ws/rest/service/v1/bp/record/file/"

    def get_bp_attach(self):
        a = get_bp_attach.GetAttach(self.accesstoken, self.path_dir)
        self.bpname, self.project_number = a.get_input()
        self.endpoint_url = self.endpoint_url + self.project_number
        a.get_attach('in_files', "get_attach.json")

    def get_data(self):
        with open(os.path.join(self.path_dir, 'in_files', 'get_attach.json'), 'r') as jfile:
            data = json.load(jfile)

        # data.pop("message")
        # data.pop("status")
        d = data["data"][0]["record_data"]
        zip_file = data["data"][0]["file_name"]
        file_content = data["data"][0]["file_handler"]
        file_size = data["data"][0]["file_size"]
        data_attach = data["data"][0]["record_data"]["attachment"]
        data["data"].pop(0)
        data["data"].append(d)

        dict1 = dict()
        dict1["options"] = {"bpname": self.bpname}
        dict1["data"] = list(data["data"])
        print(dict1["data"])
        dict1["_attachment"] = {"zipped_file_name": zip_file, "zipped_file_size": str(file_size),
                                "zipped_file_content": file_content}
        dict1["data"][0].pop("attachment")
        dict1["data"][0]["_attachment"] = data_attach
        dict1["data"][0]["nyu_val_attach_cb"] = "1"
        dict1["data"][0].pop("nyu_si_project_type")
        dict1["data"][0].pop("record_no")
        dict1["data"][0]["inv_invoice_num1"] = dict1["data"][0]["inv_invoice_num1"] + "-test"
        self.data = dict1
        # json_object = json.dumps(dict1, indent=4)
        # with open(os.path.join(self.path_dir, 'in_files', "create_inter_record.json"), "w") as outfile:
        #     outfile.write(json_object)

    def create_attach(self):
        r = requests.post(url=self.endpoint_url, json=self.data,
                          headers={'Authorization': 'Bearer {}'.format(self.accesstoken)})
        records_test = r.json()
        record_status = dict()
        record_status["record_status"] = records_test["message"][0]["_record_status"]
        record_status["status"] = records_test["status"]
        json_object = json.dumps(record_status, indent=4)
        with open(os.path.join(self.path_dir, 'out_files', "create_record.json"), "w") as outfile:
            outfile.write(json_object)


if __name__ == "__main__":
    file, path = main.file, main.path
    ac = accesstoken.AccessToken(file)
    a_token = ac.get_accesstoken()
    c = CreateAttach(a_token, path)
    c.get_bp_attach()
    c.get_data()
    # c.create_attach()
