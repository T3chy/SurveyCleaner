import re
def parseJobsTxt(txtfile):
    jobsfile = open(txtfile, 'r')
    jobs = []
    jobtitle= ""
    thisjob = []
    for line in jobsfile:
        if ":" in line:
            jobs.append([jobtitle, thisjob])
            jobtitle = line.strip("\n").strip(":")
            thisjob = []
        else:
            try:
                thisjob.append(re.sub("\/\/.*", "", line.strip("\n").strip("\t").lower()))
            except:
                print("bruh")
                thisjob.append(re.sub("\/\/.*", "", line.strip("\n").strip("\t")))
    jobs.pop(0)
    return jobs
