from pydriller import Repository,Git
import csv
import pandas as pd
import json,ast
import re

str_to_check = ['tensorflow','tensor','keras','train','training','validation','validating','cluster','matrix',
                'model','supervised','unsupervised','learning','cnn','rnn','knn','neural network','feedback loop',
              'k-means','k means','lstm','deep learning','machine learning','regression','loss function',
              'one hot encoding','backpropagation','svm','naive bayes','cross entropy',
              'classification','softmax','sigmoid','random forest','pytorch','early stop',
              'flatten','flattening','layer','nearest neighbour','gradient descent','perceptron',
              'sequential','dropout','batch size','input shape','activation function','tf idf','word2vec',
              'pattern recognition','epoch','relu','decision tree',r'\bml','validate','nlp','perceptron','pooling','convolution',
                'weight','[ml]']

a = int(input("Enter 1 for Java and 2 for Python:\n"))
projectList = []
data = pd.read_csv("data/MLSA Info.csv")
if a == 1:
    projectList = data['Java MLSA'].tolist()
elif a == 2:
    projectList = data['Python MLSA'].tolist()

dir='data/'
total=0
for pName in projectList:
    projectName=dir+pName
    gr = Git(projectName)
    data = pd.read_csv("data/"+pName+"_Fix.csv")
    fixCommits = data['FixCL'].tolist()
    data['newBuggyCLList'] = data['BuggyCLList'].apply(lambda x: ast.literal_eval(x))
    buggyCommits = data['newBuggyCLList'].tolist()
    with open("data/"+pName+'_MLCommitsViaCommitMsg.csv', 'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['FixCL'])
        print(projectName)
        #print(len(fixCommits))
        i=0
        idx=0
        for commit in fixCommits:
            fix_commit = gr.get_commit(commit)
            buggy_list = buggyCommits[idx]
            if len(buggy_list) == 0:
                idx += 1
                continue
            for str in str_to_check:
                if ((str != r'\bml\b' and str in fix_commit.msg.lower()) or (str == r'\bml\b' and re.search(str, fix_commit.msg.lower()))):
                    modList = fix_commit.modified_files
                    isJavaFile = False;
                    for modfile in modList:
                        if (modfile.new_path != None and modfile.new_path.endswith('.java')  and
                                not (modfile.new_path.find('examples\\') > -1 or modfile.new_path.find(
                                    'examples_tests\\') > -1
                                     or modfile.new_path.find('test\\') > -1 or modfile.new_path.find('tests\\') > -1
                                     or modfile.new_path.find('docs\\') > -1 or modfile.new_path.find('doc\\') > -1
                                     or modfile.new_path.startswith('.') or modfile.new_path.find(
                                            'requirements\\') > -1
                                     or modfile.new_path.find('example_configs\\') > -1)):
                            isJavaFile = True
                            break
                    if isJavaFile:
                        # print(fix_commit.msg)
                        # print(fix_commit.hash)
                        # print(modList[0].new_path)
                        writer.writerow([commit])
                        i += 1
                        break
            idx+=1
    file.close()
    total+=i