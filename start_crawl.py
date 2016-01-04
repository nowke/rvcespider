import os
import simplejson as json
import glob
from pprint import pprint

# Configurations

SEM_CODE = {
	1: "First",
	3: "Third",
	5: "Fifth",
}

Semesters = [1, 5]
Branches = ["CS", "BT", "CH", "CV", "EE", "EC", "IM", "IS", "IT", "ME", "TE", "EI"]
Branches_full = ["Computer Science Engineering",
                 "Bio Technology", 
                 "Chemical Engineering",
                 "Civil Engineering", 
                 "Electrical and Electronics Engg.",
                 "Electronics and Communication Engg.",
                 "Industrial Engg & Management" ,
                 "Information Science", 
                 "Instrumentation Technology", 
                 "Mechanical Engineering", 
                 "Telecommunication Engineering", 
                 "Instrumentation Technology"]

StudentTypes = ["normal", "diploma"]
Branches_associated = dict(zip(Branches, Branches_full))

def getConfigDict(sem, branch, stud_type):

    Config_dict =  {
        "BRANCHCODES":
        {
            "CS": "5687f1d86e95525d0e0000b6",
            "BT": "5687ee086e95525d0e000024",
            "CH": "5687f1796e95525d0e0000b4",
            "CV": "5687f1b26e95525d0e0000b5",
            "EE": "5687f2126e95525d0e0000b8",
            "EC": "5687f1ef6e95525d0e0000b7",
            "IM": "5687f2286e95525d0e0000b9",
            "IS": "5687f2426e95525d0e0000ba",
            "IT": "5687f2566e95525d0e0000bb",
            "ME": "5687f2e36e95525d0e0000bc",
            "TE": "5687f2fb6e95525d0e0000bd",
            "EI": "568901416e955220e1000017",
        },
        "CUR_BRANCH": branch,
        "CUR_BRANCH_CODE": "",
        "CUR_SEM": sem,
        "CUR_USN_START": "",
        "CUR_USN_END": "",
        "CUR_USN_YEAR": "",
        "CUR_BRANCH_FULL": Branches_associated[branch],
        "CUR_SEM_VAL": SEM_CODE[sem],
    }

    Config_dict["CUR_BRANCH_CODE"] = Config_dict["BRANCHCODES"][branch]

    base_year = 15
    stud_year = (sem + 1) / 2
    if stud_type == "normal":
        Config_dict["CUR_USN_START"] = "1"
        Config_dict["CUR_USN_END"] = "220"
        Config_dict["CUR_USN_YEAR"] = str(base_year - stud_year + 1)

    elif stud_type == "diploma":
        Config_dict["CUR_USN_START"] = "400"
        Config_dict["CUR_USN_END"] = "500"
        Config_dict["CUR_USN_YEAR"] = str(base_year - stud_year + 2)
        
    return Config_dict

def crawl():
    # For each semester
    for sem in Semesters:
        for branch in Branches:
            for StudType in StudentTypes:
                if (sem + 1) / 2 == 1 and StudType == "diploma":
                    continue

                config_dict = getConfigDict(sem, branch, stud_type=StudType)
                with open("config.py", 'w') as f:
                    f.write("Config_dict = " + repr(config_dict) + "\n")

                attacher = "" if StudType == "normal" else "-d"
                json_file_name = 'jsons/' + branch + str(sem) + attacher + ".json"
                os.system("scrapy crawl results -o " + json_file_name)

def join_jsons():

    for branch in Branches:
        read_files = glob.glob("jsons/" + branch + "*.json")

        out_res = []

        for f in read_files:
            with open(f, "r") as infile:
                char_count = len(infile.read())
            
            if char_count > 1:
                with open(f, "r") as infile: 

                    list_stud = json.load(infile)
                    for each_stud in list_stud:
                        out_res.append(each_stud)

        fname = "ojson/" + branch + ".json"

        with open(fname, "w") as outfile:
            outfile.write("[")
            stud_num = len(out_res)-1
            for i,stud in enumerate(out_res):
                if i == stud_num:
                    outfile.write(str(stud))
                    continue
                outfile.write(str(stud) + ",\n")
            outfile.write("]")

        # Replace all single quotes with double quotes
        with open(fname, "r") as outfile:
            big_str = outfile.read()

        big_str = big_str.replace("'", '"')
        big_str = big_str.replace('u"', '"')
        with open(fname, "w") as outfile:
            outfile.write(big_str)

def cleanup():
    os.system("rm jsons/*.json")
    os.system("rmdir jsons")

if __name__ == '__main__':
	crawl()
	join_jsons()
	cleanup()