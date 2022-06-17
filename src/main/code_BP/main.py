import os

path = os.pardir
file = "TokenGenerationdevNew.xlsx"
env = "stg"

def get_projno():
    level = int(input("Enter 1 for Company Level\nEnter 2 for Project Level\n"))
    if level == 2:
        project_no = input("Enter project no:")
    else:
        project_no = ""
    return project_no
