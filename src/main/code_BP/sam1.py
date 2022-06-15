import os


class Display:
    def dis(self):
        file = "samp.txt"
        path_dir = os.pardir
        with open(os.path.join(path_dir, 'in_files', file), 'r') as infile:
            print(infile.read())
