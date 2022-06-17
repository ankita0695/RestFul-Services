import requests
import accesstoken
import main
import json
import os
import get_bp_record


class UpdateBp:
    def __init__(self, access_token, path_dir):
        self.data = None
        # self.project_number = proj_no
        self.access_token = access_token
        self.path_dir = path_dir

    def get_data(self):
        self.gb = get_bp_record.GetBp(self.access_token, self.path_dir)
        self.bpname, self.record_no, self.project_number, self.input_params = self.gb.get_input()
        self.endpoint_url = "https://us2.unifier.oraclecloud.com/nyulangone/" + main.env + "/ws/rest/service/v1/bp/record/" \
                            + self.project_number
        n = int(input("Enter the number of columns to be updated:"))
        data = dict()
        data["record_no"] = self.record_no
        for i in range(n):
            key = input("Enter the column name:")
            ty = int(input("Enter the type of data:\n 1.int\n 2.float\n 3.null\n 4.string\n"))
            # value = 0
            if ty == 1:
                value = int(input("Enter the value:"))
            elif ty == 2:
                value = float(input("Enter the value:"))
            elif ty == 3:
                value = None
            elif ty == 4:
                value = (input("Enter the value:"))
            data[key] = value
        print(data)
        d = []
        d.append(data)
        options = dict()
        options["bpname"] = self.bpname
        record = dict()
        record["options"] = options
        record["data"] = d
        print(type(record))
        print(record)
        self.data = record
        return self.data

    def update_bp(self, data):
        # sending post request and saving response as response object
        r = requests.put(url=self.endpoint_url, json=data,
                         headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        # extracting response text
        # print(r)
        records_test = r.json()
        # print(records_test)
        json_object = json.dumps(records_test, indent=4)
        with open(os.path.join(self.path_dir, 'out_files', "update_record.json"), "w") as outfile:
            outfile.write(json_object)


if __name__ == "__main__":
    file, path = main.file, main.path
    a = accesstoken.AccessToken(file)
    a_token = a.get_accesstoken()
    u = UpdateBp(a_token, path)
    data = u.get_data()
    # u.update_bp(data)
