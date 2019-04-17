#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from collections import defaultdict
import os

RELEVANCE = os.path.abspath(os.path.join(os.getcwd(), "../test-collection/cacm.rel.txt"))

# phase 1 - task 1
BM25_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task1_res/bm25.txt"))
BM25_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/bm25_evaluation.txt"))

LUCENE_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task1_res/Lucene result.txt"))
LUCENE_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/lucene_evaluation.txt"))

TFIDF_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task1_res/tfidf.txt"))
TFIDF_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/tfidf_evaluation.txt"))

Q_LIKELIHOOD_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task1_res/query_likelihood_model.txt"))
Q_LIKELIHOOD_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/query_likelihood_evaluation.txt"))

# phase 1 - task 2
REL_FEEDBACK_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task2_res/pseudo relevance feedback.txt"))
REL_FEEDBACK_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/rel_feedback_evaluation.txt"))

STEM_QUERY_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task2_res/query time stemming.txt"))
STEM_QUERY_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/stem_query_evaluation.txt"))

# phase 1 - task 3
BM25_STOPPING_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task3_res/bm25_stopping.txt"))
BM25_STOPPING_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/bm25_stopping_evaluation.txt"))

TFIDF_STOPPING_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase1_task3_res/tfidf_stopping.txt"))
TFIDF_STOPPING_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/tfidf_stopping_evaluation.txt"))

# phase 3
REL_FEEDBACK_STOP_RESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/query_expansion_stopping_res.txt"))
REL_FEEDBACK_STOP_OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/query_expansion_stopping_evaluation.txt"))

relevance_dict = defaultdict(list)
query_result_dict = defaultdict(list)
query_result_info_dict = defaultdict(list)


# read relevance judgments from cacm.rel.txt
def read_relevance_judgments(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            l = line.strip().split(" ")
            q_id = l[0]
            doc_id = l[2]
            relevance_dict[q_id].append(doc_id)


# read query results from baseline runs
def read_query_results(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            l = line.strip().split(" ")
            if len(l) == 1:
                continue

            q_id = l[0]
            doc_id = l[2]
            rank = l[3]
            score = l[4]
            system = l[5]
            tup = ("Q0", doc_id, rank, score, system)
            query_result_info_dict[q_id].append(tup)
            if q_id in relevance_dict.keys():
                doc_id = l[2]
                query_result_dict[q_id].append(doc_id)


# recall is the proportion of relevant documents that are retrieved
def calc_recall(relevance_dict, query_result_dict):
    recall = defaultdict(list)

    for q_id, rel_docs in relevance_dict.items():
        res_rel_doc_cnt = 0
        rel_docs_len = len(rel_docs)
        q_docs = query_result_dict[q_id]

        for doc in q_docs:
            if doc in rel_docs:
                res_rel_doc_cnt += 1
            r = float(res_rel_doc_cnt / rel_docs_len)
            recall[q_id].append(r)

    return recall


# precision is the proportion of retrieved documents that are relevant
def calc_precision(relevance_dict, query_result_dict):
    precision = defaultdict(list)

    for q_id, rel_docs in relevance_dict.items():
        res_rel_doc_cnt = 0
        q_docs = query_result_dict[q_id]

        for idx, doc in enumerate(q_docs):
            if doc in rel_docs:
                res_rel_doc_cnt += 1
            p = float(res_rel_doc_cnt / (idx+1))
            precision[q_id].append(p)

    return precision


# average precision at rank 5 and 20
def calc_precision_at_rank(relevance_dict, query_result_dict, rank=5):
    precision = defaultdict(list)

    for q_id, rel_docs in relevance_dict.items():
        res_rel_doc_cnt = 0
        q_docs = query_result_dict[q_id]

        for idx, doc in enumerate(q_docs):
            if doc in rel_docs:
                res_rel_doc_cnt += 1
            p = float(res_rel_doc_cnt / (idx+1))
            precision[q_id].append(p)

    rank_p = []
    for q_id, precision_list in precision.items():
        rank_p.append(precision_list[rank - 1])

    precision_at_rank = float(sum(rank_p) / len(rank_p))
    return precision_at_rank


# MAP is calculated by calculating the mean of average precisions for all 64 queries
def calc_MAP(relevance_dict, query_result_dict):
    map_list = []

    for q_id, rel_docs in relevance_dict.items():
        res_rel_doc_cnt = 0
        q_docs = query_result_dict[q_id]
        precision = []

        for idx, doc in enumerate(q_docs):
            if doc in rel_docs:
                res_rel_doc_cnt += 1
            p = float(res_rel_doc_cnt / (idx+1))
            precision.append(p)

        avg_precision = 0
        if len(precision) > 0:
            avg_precision = float(sum(precision) / len(precision))

        map_list.append(avg_precision)

    MAP = float(sum(map_list) / len(map_list))
    return MAP


# MRR is calculated by averaging the reciprocal ranks of all 64 queries.
def calc_MRR(relevance_dict, query_result_dict):
    mrr_list = []

    for q_id, rel_docs in relevance_dict.items():
        res_rel_doc_cnt = 0
        q_docs = query_result_dict[q_id]

        rr = 0
        for idx, doc in enumerate(q_docs):
            if doc in rel_docs:
                rr = 1 / float(idx+1)
                break
        mrr_list.append(rr)

    MRR = float(sum(mrr_list) / len(mrr_list))
    return MRR


def evaluation(output):
    recall = calc_recall(relevance_dict, query_result_dict)
    precision = calc_precision(relevance_dict, query_result_dict)

    precision_at_5 = calc_precision_at_rank(relevance_dict, query_result_dict, 5)
    precision_at_20 = calc_precision_at_rank(relevance_dict, query_result_dict, 20)

    MAP = calc_MAP(relevance_dict, query_result_dict)
    MRR = calc_MRR(relevance_dict, query_result_dict)

    with open(output, "w", encoding="utf-8") as f:
        f.write("query_id,  literal,    doc_id, rank,   score,  system, recall, precision" + "\n")
        for q_id, info_list in query_result_info_dict.items():
            r = recall[q_id]
            p = precision[q_id]
            for idx, tup in enumerate(info_list):
                if len(r) == 0:
                    continue
                f.write(q_id + " ")
                f.write(tup[0] + " ")
                f.write(tup[1] + " ")
                f.write(tup[2] + " ")
                f.write(tup[3] + " ")
                f.write(tup[4] + " ")
                f.write(str(r[idx]) + " ")
                f.write(str(p[idx]) + " ")
                f.write("\n")
            f.write("p@5: " + str(precision_at_5) + ", p@20: " + str(precision_at_20) + "\n")
        f.write("MAP: " + str(MAP) + ", MRR: " + str(MRR) + "\n")


def main():
    read_relevance_judgments(RELEVANCE)

    # phase 1 - task 1 evaluation
    read_query_results(BM25_RESULT)
    evaluation(BM25_OUTPUT)
    read_query_results(LUCENE_RESULT)
    evaluation(LUCENE_OUTPUT)
    read_query_results(TFIDF_RESULT)
    evaluation(TFIDF_OUTPUT)
    read_query_results(Q_LIKELIHOOD_RESULT)
    evaluation(Q_LIKELIHOOD_OUTPUT)

    # phase 1 - task 2 evaluation
    read_query_results(REL_FEEDBACK_RESULT)
    evaluation(REL_FEEDBACK_OUTPUT)
    read_query_results(STEM_QUERY_RESULT)
    evaluation(STEM_QUERY_OUTPUT)

    # phase 1 - task 3 evaluation
    read_query_results(BM25_STOPPING_RESULT)
    evaluation(BM25_STOPPING_OUTPUT)
    read_query_results(TFIDF_STOPPING_RESULT)
    evaluation(TFIDF_STOPPING_OUTPUT)

    # phase 3 evaluation
    read_query_results(REL_FEEDBACK_STOP_RESULT)
    evaluation(REL_FEEDBACK_STOP_OUTPUT)


main()
