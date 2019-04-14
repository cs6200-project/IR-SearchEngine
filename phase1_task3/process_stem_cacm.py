corpus_path = '../test-collection/cacm_stem.txt'
corpus_dest_path = '../generated_files/stemming-corpus/'
query_path = '../test-collection/cacm_stem.query.txt'
query_dest_path = '../generated_files/stemming-query.txt'
def process_stem_corpus(corpus_path, dest_path):
    f = open(corpus_path, 'r')
    lines = f.readlines()
    text = ' '.join(lines)
    cacms = text.split('#')[1:]
    index = 1
    for cacm in cacms:
        cacm = ' '.join(cacm.split('\n')[1:])
        content = cacm
        pmcacm = cacm.split('pm')
        if len(pmcacm) == 2:
            content = pmcacm[0]+'pm'
        else:
            amcacm = cacm.split('am')
            if len(amcacm) == 2:
                content = amcacm[0]+'am'
        idxnum = (4 - len(str(index)))*'0' + str(index)
        outfile = open(dest_path+'stemming-CACM-' + idxnum+'.html', 'w')
        outfile.write(content)
        index += 1
    f.close()
def process_stem_query(query_path, query_dest_path):
    f = open(query_path, 'r')
    outfile = open(query_dest_path, 'w')
    lines = f.readlines()
    newlines = []
    idx = 1
    for line in lines:
        newlines.append(str(idx) + ' ' + line)
        idx += 1
    outfile.write('\n'.join(newlines))

if __name__ == '__main__':
    # process_stem_corpus(corpus_path, corpus_dest_path)
    process_stem_query(query_path, query_dest_path)