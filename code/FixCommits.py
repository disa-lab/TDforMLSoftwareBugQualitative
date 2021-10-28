from pydriller import Repository,Git
import csv
import re
import pandas as pd

a = int(input("Enter 1 for Java and 2 for Python:\n"))
dir='data/'
projectList = []
data = pd.read_csv("data/MLSA Info.csv")
if a == 1:
    projectList = data['Java MLSA'].tolist()
elif a == 2:
    projectList = data['Python MLSA'].tolist()

for pName in projectList:
    projectName=dir+pName
    gr = Git(projectName)
    print(gr.total_commits())                     # get total number of commits
    commit_list = set()
    kwds = [r'\bfix']
    for commit in Repository(projectName).traverse_commits():
        for str in kwds:
            var = re.search(str,commit.msg.lower())
            if var:
                commit_list.add(commit.hash)

    file = open(r"data\{}_Fix.csv".format(pName), "w+")
    writer = csv.writer(file)
    writer.writerow(['FixCL', 'BuggyCLList'])
    count = 0;
    for commit in commit_list:
        buggy_commitset = set()
        fix_commit = gr.get_commit(commit)
        buggy_commits = gr.get_commits_last_modified_lines(fix_commit)
        for bugComm in buggy_commits:
            Temp_commits = buggy_commits[bugComm]
            for i in Temp_commits:
                buggy_commitset.add(i)
        writer.writerow([fix_commit.hash,list(buggy_commitset)])
        count += 1
    file.close()