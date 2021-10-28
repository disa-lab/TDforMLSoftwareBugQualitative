from pydriller import Repository,Git
import csv
import pandas as pd
import json,ast

JavaProjectList=['AffectiveTweets','boofcv','CoreNLP','DataCleaner','deeplearning4j','DigitRecognizer',
                 'elasticsearch','elki','grobid','jenetics','jgap','knime-core','mahout',
                 'Mallet','moa','modernmt','Mutters','neo4j-nlp',
                 'smile','submarine','tablesaw','vespa']
dir='data/'
import_str = ['jsat', 'org.neuroph', 'opennlp', 'net.sf.javaml','com.rapidminer','weka','encog','ai.djl','org.ejml','org.apache.lucene',
              'org.apache.spark.mllib','ai.h2o','org.apache.solr','nz.ac.waikato.cms.weka','com.github.fracpete',
              'com.github.waikato','net.sf.meka','com.optimaize.languagedetector','org.apache.tika']

for pName in JavaProjectList:
    projectName=dir+pName
    gr = Git(projectName)
    data = pd.read_csv("data/" + pName + "_Fix.csv")
    fixCommits = data['FixCL'].tolist()
    data['newBuggyCLList'] = data['BuggyCLList'].apply(lambda x: ast.literal_eval(x))
    buggyCommits = data['newBuggyCLList'].tolist()
   # print(len(fixCommits))

    #file = open(r"G:\Commits_Txt\allennlp_MLFiles.csv", "w")
    file = open(r"data\{}_MLCommitsViaImport.csv".format(pName), "w")
    writer = csv.writer(file)
    writer.writerow(['FixCL', 'ML File List'])

    i = 0
    count = 0
    for commit in fixCommits:
       # print(i)
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
                if code and (str1 in code.lower() or str2 in code.lower()) and (modfile.new_path != None and modfile.new_path.endswith('.java') and
                                not (modfile.new_path.find('examples\\') > -1 or modfile.new_path.find(
                                    'examples_tests\\') > -1
                                     or modfile.new_path.find('test\\') > -1 or modfile.new_path.find('tests\\') > -1
                                     or modfile.new_path.find('docs\\') > -1 or modfile.new_path.find('doc\\') > -1
                                     or modfile.new_path.startswith('.') or modfile.new_path.find(
                                            'requirements\\') > -1
                                     or modfile.new_path.find('example_configs\\') > -1)):
                    file_list.add(modfile.new_path)
                    break
        if file_list:
            writer.writerow([fix_commit.hash,list(file_list)])
            count += 1
        i += 1
    file.close()
