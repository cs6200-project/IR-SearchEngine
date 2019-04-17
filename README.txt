CS 6200 Information Retrieval Final Project

Structure of Project:
    - README.txt: readme file
    - generated_files: include generated intermediates which could be reused in multiple tasks
    - test-collection: given dataset
    - phase1_task1:
        * BM25.py: build BM25 retrieval model
        * query_likelihood_model.py: build Query Likelihood Model
        * tfidf.py: build Tf/idf retrieval model
        * LuceneModel.java: build Lucene default retrieval model
        * process_cacm.py: read given data
        * inverted_index.py: build unigram indexer
        * bm25.txt: result ranked list of BM25 retrieval model
        * query_likelihood_model.txt: result ranked list of Query Likelihood Model retrieval model
        * tfidf.txt: result ranked list of Tf/idf retrieval model
        * Lucene result.txt: result ranked list of Lucene default retrieval model
    - phase1_task2:
        * pseudo_relevance_feedback.py: perform Pseudo Relevance Feedback technique on Tf/idf retrieval model
        * query_time_stemming.py: perform Query Time Stemming technique on Tf.idf retrieval model
        * pseudo relevance feedback.txt: result ranked list of Pseudo Relevance Feedback
        * query time stemming.txt: result ranked list of Query Time Stemming
    - phase1_task3:
        * BM252.py: build stemmed version of BM25 retrieval model
        * tfidf2.py: build stemmed version of Tf/idf retrieval model
        * inverted_index2.py: build stemmed version of unigram indexer
        * process_stem_cacm.py: read stemmed version of given data
        * remove_stop_words.py:
        * bm25_stemming.txt: result ranked list of stemmed version BM25 retrieval model
        * bm25_stopping.txt: result ranked list of stopped version BM25 retrieval model
        * tfidf_stemming.txt: result ranked list of stemmed version Tf/idf retrieval model
        * tfidf_stopping.txt: result ranked list of stopped version Tf/idf retrieval model
    - phase 2:
        * snippet_generation.py: generate snippets and highlight query
        * tfidf3.py: build Tf/idf retrieval model with the implementation of snippets generation and query highlight
        * inverted_index3.py: build unigram indexer
        * snippets.html: result of generated snippets
        * tfidf.txt: result ranked list of Tf/idf retrieval model
    - phase 3:
        * evaluation.py: perform effectiveness evaluation of result in terms of recall, precision, precision at rank, MAP and MRR
        * query_expansion_stopping.py: perform query expansion technique with stopping on Tf/idf retrieval model
        * query_expansion_stopping_res.txt: result ranked list of Tf/idf retrieval model with the implementation of query expansion with stopping
    - results:
        * /phase1_task1_res: all result files for task 1 in phase 1
        * /phase1_task2_res: all result files for task 2 in phase 1
        * /phase1_task3_res: all result files for task 3 in phase 1
        * /phase2: all result files for phase 2
        * /phase3: all result files for phase 3