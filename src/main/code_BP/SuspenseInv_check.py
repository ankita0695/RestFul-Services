import get_udr
import accesstoken
import main
import update_bp_record


class UniqueInvCheck:
    def __init__(self, a_token, path):
        self.g = get_udr.GetUdr(a_token, path)
        self.u = update_bp_record.UpdateBp(a_token, path)

    def getudr(self):
        self.g.get_data()
        # print(self.g.data)
        self.g.get_udr('output', "z_SusInv_NonDupInv.json")
        self.record = self.g.records_test

    def update_sus(self):
        record = dict()
        options = dict()
        wfd = dict()
        wfd["WFCurrentStepName"] = "Duplicate Invoice Check"
        options["bpname"] = 'Suspense Invoice'
        options["workflow_details"] = wfd
        record["options"] = options
        row = dict()
        for x in self.record["data"][0]["report_header"]:
            if self.record["data"][0]["report_header"][x]['name'] == 'UNIQUEINVOICECHECK':
                u_inv_check = x
            elif self.record["data"][0]["report_header"][x]['name'] == 'RECORD_NO':
                rec_no = x
        # print(u_inv_check, rec_no)
        for i in range(0, len(self.record["data"][0]["report_row"])):
            row["record_no"] = self.record["data"][0]["report_row"][i][rec_no]
            if self.record["data"][0]["report_row"][i][u_inv_check] == 'UniqueInvoice':
                row["nyu_si_reason_code"] = "Process"
                wfd["WFActionName"] = "Approve"
            else:
                row["nyu_si_reason_code"] = "Already in UNF"
                wfd["WFActionName"] = "Closed"
            record["data"] = []
            record["data"].append(row)
            print(i, ":", record)
            # self.u.update_bp(record)


if __name__ == "__main__":
    file, path = main.file, main.path
    a = accesstoken.AccessToken(file)
    a_token = a.get_accesstoken()
    u = UniqueInvCheck(a_token, path)
    u.getudr()
    u.update_sus()