# -*- coding: utf-8 -*-
import os

corpus_dir = '../generated_files/corpus'

save_index_path = '../generated_files/index.txt'
save_doc_length_path = '../generated_files/doc_length.txt'
save_tf_path = '../generated_files/tf.txt'


def get_inverted_index(corpus_path):
    file_list = os.listdir(corpus_path)
    index = {}
    doc_len = {}
    for filename in file_list:
        if filename[0] == '.':
            continue
        doc_id = filename[:-5]
        f = open(corpus_path + '/' + filename, 'r')
        uni_grams = f.read().split()
        for term in uni_grams:
            if term in index:
                if doc_id in index[term]:
                    index[term][doc_id] += 1
                else:
                    index[term][doc_id] = 1
            else:
                index[term] = {doc_id: 1}
        doc_len[doc_id] = len(uni_grams)
        f.close()
    return index, doc_len


def get_tf(index):
    tf = {}
    for key in index:
        t_freq = 0
        for k in index[key]:
            t_freq += index[key][k]
        tf[key] = t_freq
    return tf


def save_dict(d, filename):
    f = open(filename, 'w')
    for key in d:
        f.write(str(key) + '=> ' + str(d[key]) + '\n')
    f.close()


def save_list(l, filename):
    f = open(filename, 'w')
    for line in l:
        f.write(str(line[0]) + ': ' + str(line[1]) + '\n')
    f.close()


if __name__ == '__main__':
    inverted_index, doc_length = get_inverted_index(corpus_dir)
    tf = get_tf(inverted_index)
    tf = sorted(tf.items(), key=lambda item: item[1], reverse=True)
    save_dict(inverted_index, save_index_path)
    save_dict(doc_length, save_doc_length_path)
    save_list(tf, save_tf_path)
