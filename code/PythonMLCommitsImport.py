from pydriller import Repository,Git
import csv
import pandas as pd
import json,ast

pythonProjectList=['ray','deepchem','chainercv','tensor2tensor',
                   'ml-agents','NiftyNet','tensorpack','DeepPavlov','OpenNMT-py','allennlp','tpot',
                  'MatchZoo','texar','OpenSeq2Seq','bert-as-service','catalyst','deepvariant',
                   'horovod','luminoth','astroML','PyTorch-NLP','gentun'
                   ]
dir='data/'
import_str = ['sklearn','tensorflow','keras','pytorch','opencv','nltk','mxnet','pyspark.mllib']
for pName in pythonProjectList:
    projectName=dir+pName
    gr = Git(projectName)
    csvpath = "data/{}_fix.csv".format(pName)
    data = pd.read_csv(csvpath)
    fixCommits = data['FixCL'].tolist()
    data['newBuggyCLList'] = data['BuggyCLList'].apply(lambda x: ast.literal_eval(x))
    buggyCommits = data['newBuggyCLList'].tolist()
    #print(len(fixCommits))

    #file = open(r"G:\Commits_Txt\allennlp_MLFiles.csv", "w")
    file = open(r"data\{}_MLCommitsViaImport.csv".format(pName), "w")
    writer = csv.writer(file)
    writer.writerow(['FixCL', 'ML File List'])

    i = 0
    count = 0
    for commit in fixCommits:
        file_list = set()
        buggy_list = buggyCommits[i]
        if len(buggy_list) == 0:
            i += 1
            continue
        fix_commit = gr.get_commit(commit)
        modList = fix_commit.modified_files
        for modfile in modList:
            code = modfile.source_code
            for str in import_str:
                str1 = 'from {}'.format(str)
                str2 = 'import {}'.format(str)
                if code and (str1 in code.lower() or str2 in code.lower()) and (modfile.new_path != None and (modfile.new_path.endswith('.py') or
                        modfile.new_path.endswith('ipynb')) and not (modfile.new_path.startswith('examples\\') or
                                     modfile.new_path.startswith('examples_tests\\')
                                     or modfile.new_path.startswith('tests\\') or modfile.new_path.startswith('tests\\')
                                     or modfile.new_path.startswith('docs\\') or modfile.new_path.startswith('doc\\')
                                     or modfile.new_path.startswith('.') or modfile.new_path.startswith('requirements\\')
                                     or modfile.new_path.startswith('example_configs\\'))):
                    file_list.add(modfile.new_path)
                    break
        if file_list:
            writer.writerow([fix_commit.hash,list(file_list)])
            count += 1
        i += 1
    file.close()
