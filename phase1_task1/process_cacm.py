# -*- coding: utf-8 -*-
import os
import re
from bs4 import BeautifulSoup

corpus_src_dir = '../test-collection/cacm'
corpus_dest_dir = '../generated_files/corpus'

cacm_query_src = '../test-collection/cacm.query.txt'
cacm_query_dest = '../generated_files/query.txt'

re_cite = re.compile('\[[0-9.,]*\]')
re_punc = re.compile('[^0-9a-zA-Z- \n\t]+')
re_newline = re.compile('\n+')
re_space = re.compile('\\s+')


# transfer raw html generated_files to text generated_files
def get_corpus(src_dir, dest_dir):
    file_list = os.listdir(src_dir)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    for filename in file_list:
        if filename[0] == '.':
            continue
        f_open = open(src_dir + '/' + filename, 'r')
        bs = BeautifulSoup(f_open, 'html.parser')
        content = []
        for pre in bs.find_all(['pre']):
            content.append(pre.text)
        content = ' '.join(content)
        content = re_cite.sub('', content)
        content = str(content.encode('ascii', 'ignore').decode('ascii'))
        content = re_punc.sub(' ', content)
        content = content.split('\n')
        for i in range(len(content)):
            is_all_number = True
            for j in range(len(content[i])):
                if not (content[i][j] == ' ' or content[i][j] == '\t' or (content[i][j] >= '0' and content[i][j] <= '9')):
                    is_all_number = False
            if is_all_number:
                content[i] = ''
        content = ' '.join(content)
        content = content.casefold()
        content = content.strip()
        f_open.close()
        f_save = open(dest_dir + '/' + filename, 'w')
        f_save.write(content)
        f_save.close()


# extract queries from raw text
def get_query(src_file, dest_file):
    f = open(src_file, 'r')
    content = f.read()
    f.close()
    raw_text = []
    bs = BeautifulSoup(content, 'lxml')
    for text in bs.find_all('doc'):
        raw_text.append(text.text.strip())
    query_dict = {}
    for q in raw_text:
        q = q.split(' ', 1)
        query_content = q[1].strip()
        query_content = str(query_content.encode('ascii', 'ignore').decode('ascii'))
        query_content = re_punc.sub(' ', query_content)
        query_content = re_newline.sub(' ', query_content)
        query_content = re_space.sub(' ', query_content)
        query_content = query_content.casefold()
        query_dict[int(q[0])] = query_content
    f = open(dest_file, 'w')
    sorted(query_dict.keys())
    for key in query_dict:
        f.write(str(key) + ' ' + query_dict[key] + '\n')
    f.close()


if __name__ == '__main__':
    get_corpus(corpus_src_dir, corpus_dest_dir)
    get_query(cacm_query_src, cacm_query_dest)
