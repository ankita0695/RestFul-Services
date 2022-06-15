import json
import requests
import os
import accesstoken
import main


class GetBp:
    def __init__(self, access_token, path_dir):
        self.access_token = access_token
        self.path_dir = path_dir
        self.project_number = None
        self.input_params = "\"bpname\": \"%s\", \"record_no\": \"%s\", \"lineitem\": \"%s\""

    def get_input(self):
        self.project_number = main.get_projno()
        bpname = input("Enter the BP name:")
        record_no = input("Enter the record no:")
        line_item = input("Line item yes or no:")
        self.input_params = self.input_params % (bpname, record_no, line_item)
        return bpname, record_no, self.project_number, self.input_params

    def get_bp(self, out_path, out_file):
        # api-endpoint
        endpoint_url = "https://us2.unifier.oraclecloud.com/nyulangone/dev/ws/rest/service/v1/bp/record/" \
                       + self.project_number + "?input={" + self.input_params + "}"
        # sending get request and saving the response as response object
        r = requests.get(url=endpoint_url, headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        # extracting data in json format
        data = r.json()
        json_object = json.dumps(data, indent=4)
        with open(os.path.join(self.path_dir, out_path, out_file), "w") as outfile:
            outfile.write(json_object)


if __name__ == "__main__":
    file, path = main.file, main.path
    a = accesstoken.AccessToken(file)
    a_token = a.get_accesstoken()
    g = GetBp(a_token, path)
    g.get_input()
    g.get_bp('out_files', 'get_BP_record.json')
