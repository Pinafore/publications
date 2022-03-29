#!/bin/bash
sftp test1 << EOF
    get /exp/myuan/userstudy/day1/session1/time_full.jsonl session1_full.jsonl
    get /exp/myuan/userstudy/day1/session2/time_full.jsonl session2_full.jsonl
    get /exp/myuan/userstudy/day1/session1/time_reduced.jsonl session1_reduced.jsonl
    get /exp/myuan/userstudy/day1/session2/time_reduced.jsonl session2_reduced.jsonl

    get /exp/myuan/userstudy/study_scores.jsonl study_scores.jsonl
    get /exp/myuan/simulation/spb_preco_24_2500/results_test.csv results_preco.csv
    get /exp/myuan/simulation/qb_0_24_240/results_test.csv results_qbcoref.csv
EOF
