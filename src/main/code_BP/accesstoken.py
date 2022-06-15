import openpyxl
import os


class AccessToken:
    def __init__(self, file):
        self.access_token = None
        self.file = file

    def get_accesstoken(self):
        wk = openpyxl.load_workbook(os.path.join(os.pardir, 'in_files', self.file))
        sh = wk.active
        c = sh.cell(row=2, column=1)
        self.access_token = c.value
        return self.access_token
