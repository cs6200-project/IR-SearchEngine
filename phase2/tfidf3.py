# -*- coding: utf-8 -*-
import math
from phase2.snippet_generation import get_snippet
index_path = 'index.txt'
doc_len_path = 'doc_length.txt'
query_path = '../generated_files/query.txt'
result_path = 'tfidf.txt'


class tfidf_model:
    def __init__(self, index_file, doc_len_file, query_file, result_file, top_res_num=100):
        self.__get_index(index_file)
        self.__get_doc_len(doc_len_file)
        self.__get_query(query_file)
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

    def __score(self, freq, doc_id, term_length):
        return ((freq + 0.0) / self.doc_len[doc_id]) * (1 + math.log(len(self.doc_len) / (term_length + 1)))

    def search(self):
        f = open(self.result_file, 'w')
        fsnippet = open("snippets.html", 'w')
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
            count = 0
            for line in score:
                count += 1
                f.write(str(key) + ' Q0 ' + line[0] + ' ' + str(count) + ' ' + str(line[1]) + ' TFIDF\n')
                get_snippet("../test-collection/cacm/"+line[0]+".html", self.query[key], str(key) + ' Q0 ' + line[0] + ' ' + str(count) + ' ' + str(line[1]) + ' TFIDF\n',fsnippet)
                if count >= self.top_res:
                    break
        f.close()


if __name__ == '__main__':
    model = tfidf_model(index_path, doc_len_path, query_path, result_path)
    model.search()
