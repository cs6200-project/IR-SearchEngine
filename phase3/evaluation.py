#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from collections import defaultdict
import os

RELEVANCE = os.path.abspath(os.path.join(os.getcwd(), "../test-collection/cacm.rel.txt"))
RUNRESULT = os.path.abspath(os.path.join(os.getcwd(), "../results/***/***.txt"))
OUTPUT = os.path.abspath(os.path.join(os.getcwd(), "../results/phase3/***.txt"))

relevance_dict = defaultdict(list)
query_result_dict = defaultdict(list)


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
            q_id = l[0]
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


def evaluation(output=""):
    recall = calc_recall(relevance_dict, query_result_dict)
    print("Recall: ", str(recall))
    precision = calc_precision(relevance_dict, query_result_dict)
    print("Precision: ", str(precision))
    precision_at_5 = calc_precision_at_rank(relevance_dict, query_result_dict, 5)
    precision_at_20 = calc_precision_at_rank(relevance_dict, query_result_dict, 20)
    print("P@5: ", precision_at_5)
    print("P@20: ", precision_at_20)
    MAP = calc_MAP(relevance_dict, query_result_dict)
    print("MAP: ", MAP)
    MRR = calc_MRR(relevance_dict, query_result_dict)
    print("MRR", MRR)


def main():
    read_relevance_judgments(RELEVANCE)
    read_query_results(RUNRESULT)
    evaluation()


main()
