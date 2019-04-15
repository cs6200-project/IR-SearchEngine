# -*- coding: utf-8 -*-
import math
import os
from collections import Counter

corpus_path = '../corpus'
index_path = '../index.txt'
doc_len_path = '../doc_length.txt'
query_path = '../query.txt'
result_path = 'query_likelihood_model.txt'


class query_likelihood_model:
    def __init__(self, corpus_dir, index_file, doc_len_file, query_file, result_file, top_res_num=100):
        self.__get_index(index_file)
        self.__get_doc_len(doc_len_file)
        self.__get_query(query_file)
        self.__get_corpus(corpus_dir)
        self.result_file = result_file
        self.top_res = top_res_num
        self.mu = 2000

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
        self.c = 0
        for filename in file_list:
            if filename[0] == '.':
                continue
            f = open(path + '/' + filename, 'r')
            content = f.read()
            self.corpus[filename.replace('.html', '')] = content.split()
            if self.c == 0:
                self.c_count = Counter(self.corpus[filename.replace('.html', '')])
            else:
                self.c_count = self.c_count + Counter(self.corpus[filename.replace('.html', '')])
            self.c += len(self.corpus[filename.replace('.html', '')])
            f.close()

    def __score(self, q, doc_id):
        freq = Counter(self.corpus[doc_id])[q]
        d = len(self.corpus[doc_id])
        fc = self.c_count[q]
        temp = (freq + self.mu * fc / self.c) / (d + self.mu)
        if temp == 0:
            return 0
        else:
            return math.log(temp)

    def search(self):
        f = open(self.result_file, 'w')

        for key in sorted(self.query.keys()):
            score = {}
            query_terms = self.query[key].split()
            for q in query_terms:
                if q not in self.index:
                    continue
                for doc_id in self.index[q]:
                    s = self.__score(q, doc_id)
                    if doc_id in score:
                        score[doc_id] += s
                    else:
                        score[doc_id] = s
            score = sorted(score.items(), key=lambda item: item[1], reverse=True)
            count = 0
            for line in score:
                count += 1
                f.write(str(key) + ' Q0 ' + line[0] + ' ' + str(count) + ' ' + str(line[1]) + ' QUERY_LIKELIHOOD\n')
                if count >= self.top_res:
                    break
        f.close()


if __name__ == '__main__':
    model = query_likelihood_model(corpus_path, index_path, doc_len_path, query_path, result_path)
    model.search()


