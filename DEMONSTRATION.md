# Demonstration — approximately 6 minutes

## 1. Launch and explain the model (30 seconds)

Run `python server.py`, open http://127.0.0.1:8000. Nodes are arguments; arrows are attacks. The left panel edits the graph, ownership, revealed reports, and test set S. The engine computes every displayed result in Python.

## 2. Defence and semantics (one minute)

Choose **Defence chain**: a → b → c. Set S to `a` and analyse. It is conflict-free and admissible, but not complete; it defends a and c. The grounded extension is {a,c}. Change S to `a,c`: it is complete.

Choose **Mutual attack** and select complete semantics. Extensions are {}, {a}, {b}; preferred and stable omit {}. Under preferred semantics, a and b are credulously accepted. Legal labellings are undec/undec, in/out, and out/in.

Choose **Odd cycle** and stable semantics. There is no stable extension; stable acceptance is undefined. Under grounded semantics, every node is undecided even though acceptance status is “rejected”.

## 3. Book Example 5.10: profitable hiding (90 seconds)

Choose **Profitable hiding**. Here a1 means alpha_1 in the book. Agent x (0) owns a1,a4,a5; y (1) owns a2; z (2) owns a3. Under full revelation the outcome is {a1,a3}, with utilities [1,0,1]. These utilities correct the swapped ownership in the printed example.

In the Reports box remove a1 from the first line, leaving `a4,a5`; keep the other lines `a2` and `a3`. Analyse. The outcome is {a2,a4,a5}; x's utility rises to 2. Expand the best-response section to see every optimal report. The exact strategyproofness test searches all opponents' possible reports, not merely the currently displayed reports.

## 4. Book Example 5.11: sufficient is not necessary (one minute)

Choose **Protective defender**. Agent x additionally owns a6, which attacks a3. All four of x's arguments are accepted under full revelation. The exact test reports strategyproof even though the odd-walk condition fails. a6 cancels the harmful indirect defeat; the book's a5 reference is a misprint. The program verifies every opponent report as well as the full-revelation profile.

## 5. Experiments and reproducibility (one minute)

Open `results/summary.csv`: there are 1,000 instances at each of five p values. Strategyproofness fractions are 0.811, 0.181, 0.021, 0.007, and 0.000. No condition-passing graph fails the exact test. There are 709 strategyproof graphs failing the condition. `instances.jsonl` retains every graph and its classification; profitable deviations include the opponent profile and gain. `case_studies.json` selects actual examples.

## 6. Automated evidence (one minute)

Run `python -m unittest -v` and `python demo.py`. The tests include both book examples, cycles, validation, and all 512 three-node graphs checked against an independent total-labelling definition. `results/demo.txt` contains a saved executable demonstration transcript. Use Export JSON in the UI to save a custom analysis.
