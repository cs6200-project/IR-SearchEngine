# -*- coding: utf-8 -*-
import math
import os
from collections import Counter

corpus_path = '../corpus'
index_path = '../index.txt'
doc_len_path = '../doc_length.txt'
query_path = '../query.txt'
result_path = 'bm25.txt'


class bm25_model:
    K1 = 1.2
    B = 0.75
    K2 = 100

    def __init__(self, corpus_dir, index_file, doc_len_file, query_file, result_file, top_res_num=100):
        self.__get_index(index_file)
        self.__get_doc_len(doc_len_file)
        self.__get_query(query_file)
        self.__get_corpus(corpus_dir)
        self.result_file = result_file
        self.top_res = top_res_num

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
        self.length = {}
        self.average_len = 0
        for filename in os.listdir(path):
            if filename[0] != '.' and filename.find('.html') > 0:
                f = open(path + '/' + filename, 'r')
                content = f.read().split()
                self.length[filename.replace('.html', '')] = len(content)
                self.average_len += len(content)
                f.close()
        self.N = len(self.length)
        self.average_len /= self.N

    def __score(self, doc_id, q):
        _score = 0
        K = self.K1 * ((1 - self.B) + self.B * self.length[doc_id] / self.average_len)
        for word in q.split():
            if word not in self.index or doc_id not in self.index[word]:
                continue
            tf = self.index[word][doc_id]
            qf = Counter(q.split())[word]
            df = len(self.index[word])
            _score += math.log(((self.K1 + 1) * tf * (self.K2 + 1) * qf * (self.N - df + 0.5)) / (
                        (df + 0.5) * (self.K2 + qf) * (K + tf)))
        return _score

    def search(self):
        f = open(self.result_file, 'w')

        for key in sorted(self.query.keys()):
            score = {}
            for doc_id in self.length.keys():
                score[doc_id] = self.__score(doc_id, self.query[key])
            score = sorted(score.items(), key=lambda item: item[1], reverse=True)
            count = 0
            for line in score:
                count += 1
                f.write(str(key) + ' Q0 ' + line[0] + ' ' + str(count) + ' ' + str(line[1]) + ' BM25\n')
                if count >= self.top_res:
                    break
        f.close()


if __name__ == '__main__':
    model = bm25_model(corpus_path, index_path, doc_len_path, query_path, result_path)
    model.search()
