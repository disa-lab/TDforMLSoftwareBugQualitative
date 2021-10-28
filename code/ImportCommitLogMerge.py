from pydriller import Repository,Git
import csv
import pandas as pd
import json,ast

dir='data/'
a = int(input("Enter 1 for Java and 2 for Python:\n"))
projectList = []
data = pd.read_csv("data/MLSA Info.csv")
if a == 1:
    projectList = data['Java MLSA'].tolist()
elif a == 2:
    projectList = data['Python MLSA'].tolist()

for pName in projectList:
    print(pName)
    df=pd.read_csv("data/{}_MLCommitsViaCommitMsg.csv".format(pName))
    df1=pd.read_csv("data/{}_MLCommitsViaImport.csv".format(pName))
    result=df1.merge(df,on="FixCL",how='outer') #outer join

    csvpath = "data/{}_cmt_import_merge_sorted.csv".format(pName)
    result.to_csv(csvpath, index=False) #merged file

    df = pd.read_csv(csvpath)
    fixCommits = df['FixCL'].tolist()
    print(len(fixCommits))

    totalModifiedFiles=list()
    for commit in fixCommits:
        gr = Git(dir+pName)
        fix_commit = gr.get_commit(commit)
        numFiles = fix_commit.files
        totalModifiedFiles.append(numFiles)

    df['TotalModFiles']=totalModifiedFiles
    df.to_csv(csvpath, index=False) #Add TotalModFiles Column

    sorted_df = df.sort_values(by='TotalModFiles')
    sorted_df.to_csv(csvpath, index=False)  #sort by TotalModFiles
