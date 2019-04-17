#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# -*- coding: utf-8 -*-
import math
import os
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

corpus_path = '../generated_files/corpus'
index_path = '../generated_files/index.txt'
doc_len_path = '../generated_files/doc_length.txt'
query_path = '../generated_files/query.txt'
result_path = 'query_expansion_stopping_res.txt'


class tfidf_model_pseudo_relevance_feedback:
    def __init__(self, corpus_dir, index_file, doc_len_file, query_file, result_file, top_res_num=100):
        self.__get_corpus(corpus_dir)
        self.__get_index(index_file)
        self.__get_doc_len(doc_len_file)
        self.__get_query(query_file)
        self.result_file = result_file
        self.top_res = top_res_num
        self.dice_window_size = 10

    def __get_index(self, filename):
        self.index = {}
        f = open(filename, 'r')
        line = f.readline()
        while line:
            line = line.split('=> ')
            self.index[line[0]] = eval(line[1])
            line = f.readline()
        f.close()

    def __get_doc_len(self, filename):
        self.doc_len = {}
        f = open(filename, 'r')
        line = f.readline()
        while line:
            line = line.split('=> ')
            self.doc_len[line[0]] = int(line[1])
            line = f.readline()
        f.close()

    def __get_query(self, filename):
        self.query = {}
        f = open(filename, 'r')
        line = f.readline()
        while line:
            line = line.split(' ')
            q = ' '.join(line[1:])
            self.query[int(line[0])] = q
            line = f.readline()
        f.close()

    def __get_corpus(self, path):
        self.corpus = {}
        file_list = os.listdir(path)
        for filename in file_list:
            if filename[0] == '.':
                continue
            f = open(path + '/' + filename, 'r')
            content = f.read()
            self.corpus[filename.replace('.html', '')] = content.split()
            f.close()

    def __score(self, freq, doc_id, term_length):
        return ((freq + 0.0) / self.doc_len[doc_id]) * (1 + math.log(len(self.doc_len) / (term_length + 1)))

    def __pseudo_relevance_feedback(self, init_query, top_docs, top_num=5):
        tc = 0
        qc = {}
        qtc = {}
        sw = stopwords.words('english')
        for i in range(top_num):
            for j in range(len(self.corpus[top_docs[i][0]]) - self.dice_window_size):
                is_contain = False
                for k in range(self.dice_window_size):
                    if self.corpus[top_docs[i][0]][j + k] in init_query and self.corpus[top_docs[i][0]][j + k] not in sw:
                        is_contain = True
                        break
                if is_contain:
                    tc += 1
                    for k in range(self.dice_window_size):
                        if self.corpus[top_docs[i][0]][j + k] in sw:
                            continue
                        if self.corpus[top_docs[i][0]][j + k] not in init_query:
                            if self.corpus[top_docs[i][0]][j + k] in qtc:
                                qtc[self.corpus[top_docs[i][0]][j + k]] += 1
                            else:
                                qtc[self.corpus[top_docs[i][0]][j + k]] = 1
            for j in range(len(self.corpus[top_docs[i][0]]) - self.dice_window_size):
                for k in range(self.dice_window_size):
                    if self.corpus[top_docs[i][0]][j + k] in qtc:
                        if self.corpus[top_docs[i][0]][j + k] in qc:
                            qc[self.corpus[top_docs[i][0]][j + k]] += 1
                        else:
                            qc[self.corpus[top_docs[i][0]][j + k]] = 1
        termCount = {}
        for key in qtc:
            termCount[key] = qtc[key]/(qc[key] + tc + 0.0)
        termCount = sorted(termCount.items(), key=lambda item: item[1], reverse=True)
        for i in range(6):
            init_query.append(termCount[i][0])

    def search(self):
        f = open(self.result_file, 'w')

        for key in sorted(self.query.keys()):
            score = {}
            query_terms = self.query[key].split()
            for q in query_terms:
                if q not in self.index:
                    continue
                for doc_id in self.index[q]:
                    doc_freq = self.index[q][doc_id]
                    s = self.__score(doc_freq, doc_id, len(self.index[q]))
                    if doc_id in score:
                        score[doc_id] += s
                    else:
                        score[doc_id] = s
            score = sorted(score.items(), key=lambda item: item[1], reverse=True)
            self.__pseudo_relevance_feedback(query_terms, score)
            score = {}
            for q in query_terms:
                if q not in self.index:
                    continue
                for doc_id in self.index[q]:
                    doc_freq = self.index[q][doc_id]
                    s = self.__score(doc_freq, doc_id, len(self.index[q]))
                    if doc_id in score:
                        score[doc_id] += s
                    else:
                        score[doc_id] = s
            score = sorted(score.items(), key=lambda item: item[1], reverse=True)
            count = 0
            for line in score:
                count += 1
                f.write(str(key) + ' Q0 ' + line[0] + ' ' + str(count) + ' ' + str(line[1]) + ' PSEUDO_RELEVANCE_FEEDBACK_STOPPING\n')
                if count >= self.top_res:
                    break
        f.close()


if __name__ == '__main__':
    model = tfidf_model_pseudo_relevance_feedback(corpus_path, index_path, doc_len_path, query_path, result_path)
    model.search()
