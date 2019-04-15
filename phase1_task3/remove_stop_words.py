import os
common_words_path = '../test-collection/common_words'

def remove_corpus_stop_words(corpus_path):
    file_list = os.listdir(corpus_path)
    stop_words = get_stop_words()
    for filename in file_list:
        filtered_words = []
        newfn = "stopping-" + filename
        f = open(corpus_path + '/' + filename, 'r')
        uni_grams = f.read().split()
        for term in uni_grams:
            if term in stop_words:
                continue
            else:
                filtered_words.append(term)
        f.close()
        outfile = open('../generated_files/' + newfn, 'w')
        outfile.write(" ".join(filtered_words))

def remove_query_stop_words(query_path):
    stop_words = get_stop_words()
    f = open('../generated_files/query.txt', 'r')
    lines = []
    for line in f.readlines():
        terms = line.split()
        newterms = []
        for term in terms:
            if term in stop_words:
                continue
            else:
                newterms.append(term)
        lines.append(" ".join(newterms))
    f.close()
    outfile = open('../generated_files/stopping-query.txt', 'w')
    outfile.write("\n".join(lines))

def get_stop_words():
    f = open(common_words_path, 'r')
    stop_words = f.read().split()
    return stop_words
def delte_stopping():
    f = open('bm25_stemming.txt', 'r')
    lines = []
    for line in f.readlines():
        lines.append(''.join(line.split('stemming-')))
    f.close()
    outfile = open('bm25_stemming.txt', 'w')
    outfile.write("\n".join(lines))
if __name__ == '__main__':
    # remove_corpus_stop_words('../generated_files/corpus')
    # remove_query_stop_words('../generated_files/query.txt')
    delte_stopping()