import requests
import accesstoken
import main
import json
import os


class GetUdr:
    def __init__(self, access_token, path_dir):
        self.data = None
        self.access_token = access_token
        self.path_dir = path_dir
        # self.data = {"reportname": "All_PO_Records_Test"}
        # defining the api-endpoint /ws/rest/service/v1/data/udr/get/    /ws/rest/service/v1/bp/record/
        self.endpoint_url = "https://us2.unifier.oraclecloud.com/nyulangone/dev/ws/rest/service/v1/data/udr/get/"

    def get_data(self):
        report_name = input("Enter the UD Report name:")
        self.data = {"reportname": report_name}

    def get_udr(self, out_folder, out_file):
        # sending post request and saving response as response object
        r = requests.post(url=self.endpoint_url, json=self.data,
                          headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        # extracting response text
        # print(r)
        self.records_test = r.json()
        # print(records_test)
        # print("Write file")
        json_object = json.dumps(self.records_test, indent=4)
        with open(os.path.join(self.path_dir, out_folder, out_file), "w") as outfile:
            outfile.write(json_object)
            # print("File successfully written")


if __name__ == "__main__":
    file, path = main.file, main.path
    a = accesstoken.AccessToken(file)
    a_token = a.get_accesstoken()
    # print(a_token)
    g = GetUdr(a_token, path)
    g.get_data()
    g.get_udr('out_files', "get_udr.json")
