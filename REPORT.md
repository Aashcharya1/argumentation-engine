# Argumentation Engine and Strategic Revelation

**Course:** Autonomous Systems E2E

**Implementation:** Python 3.10+, standard library; HTML/CSS/JavaScript local frontend

**Experiment:** 5,000 seeded instances; three agents; 6–8 arguments

## 1. Objective and source identification

This project computes abstract argumentation semantics and tests whether agents can benefit by hiding arguments under a grounded direct mechanism. It includes exact algorithms, validation, a visual interface, and reproducible experimental evidence.

The matching textbook is Gerhard Weiss (editor), *Multiagent Systems*, second edition, MIT Press, 2013. Chapter 5, “Argumentation Among Agents,” is by Iyad Rahwan (pp. 177–210). The author bibliography confirms the chapter, and the publisher contents confirm its placement. The indexed book text matches Theorems 5.3–5.4 and Examples 5.10–5.11. References are provided below. These two strategic examples are implemented directly; additional small regression graphs exercise the semantics. This submission does not claim to reproduce every figure in the chapter.

The assignment's pasted p values are missing. We explicitly choose p ∈ {0.1,0.3,0.5,0.7,0.9}. Each probability receives 1,000 instances, exceeding 1,000 total. This grid can be changed using the experiment CLI.

## 2. Formal model and semantics

An argumentation framework is AF = (A,R), with finite arguments A and directed attacks R ⊆ A×A. For S ⊆ A, define S⁺ = {b : some a ∈ S attacks b}. The implementation stores sets as immutable frozensets and rejects unknown attack endpoints.

| Operation | Implemented definition |
|---|---|
| Conflict-free | S ∩ S⁺ = ∅ |
| Defence of a by S | Every attacker of a belongs to S⁺ |
| Characteristic F(S) | All arguments defended by S |
| Admissible | Conflict-free and S ⊆ F(S) |
| Complete | Conflict-free and S = F(S) |
| Grounded | Least fixed point of F, iterated from ∅ |
| Preferred | Inclusion-maximal admissible sets |
| Stable | Conflict-free and S ∪ S⁺ = A |
| Semi-stable | Complete sets with inclusion-maximal range S ∪ S⁺ |

Finite monotone characteristic iteration terminates at the grounded extension. Other extension families enumerate all subsets. Inclusion-maximality matters: selecting only sets of greatest cardinality would be incorrect for preferred or semi-stable semantics.

Each complete extension E yields a total legal labelling: in = E, out = E⁺, undec = A \ (E ∪ E⁺). Equivalently, a node is in exactly when all attackers are out, out exactly when some attacker is in, and undec otherwise. This bijection generates all legal labellings without enumerating all 3^n assignments in normal operation.

Acceptance is relative to a requested semantics: skeptical if in every extension; credulous-only if in some but not every extension; rejected if in none. Skeptical acceptance mathematically implies credulous acceptance when extensions exist; the API returns the strongest category. If the extension family is empty (possible for stable semantics), the API reports undefined. Rejection is an extension-membership category, so a rejected argument can still be undecided rather than out.

## 3. Grounded direct mechanism and strategic checks

Ownership A₁,…,Aₖ partitions A. A report Rᵢ is any subset of Aᵢ, including ∅. The mechanism returns the grounded extension of the graph induced by ∪Rᵢ. Attacks involving hidden arguments disappear; attacks between remaining arguments are preserved.

Utility is uᵢ(R) = |Aᵢ ∩ G(R)|. It counts accepted arguments owned by the agent. `best_responses` enumerates every possible report against fixed reports by the others and returns all reports attaining maximum utility, including truthful reports when tied.

The exact Theorem 5.3 check tests, for every agent and every opponents' report profile:

uᵢ(Aᵢ,R₋ᵢ) ≥ uᵢ(Tᵢ,R₋ᵢ) for every Tᵢ ⊆ Aᵢ.

A failure returns a concrete profitable deviation with the opponents' reports, truthful utility, best utility, and all best reports for that profile. A pass requires checking every profile. Early stopping on a counterexample is logically sufficient for a failure. Ties are allowed: truthfulness need only be a weakly dominant strategy. Outcomes are cached by revealed union.

The Theorem 5.4 implementation tests the absence of odd directed reachability between arguments of the same agent. It is a **sufficient certificate**, not an equivalent strategyproofness test. Failing it does not prove manipulability.

### Cycles and the meaning of path

We use a conservative walk-based interpretation of indirect defeat: repeated vertices are allowed, and positive odd returns to the same argument count. BFS operates on states (argument, parity). An edge flips parity; reaching (b,odd) from (a,even) witnesses an odd walk. There are at most 2n states per source, so cycles cannot cause infinite traversal. Parent pointers return a concrete witness.

A simple-path interpretation forbidding repeated vertices is a different property in cyclic graphs. This report and the result metadata use the walk convention explicitly. The no-odd-walk condition implies absence of odd simple paths; its failure can include cycle-related conservative false negatives. Exact strategyproofness remains unaffected by this convention. Direct internal attacks, including self-attacks, violate the condition automatically.

## 4. Textbook regression cases and errata

`book_examples.py` reproduces the two strategic graphs using a1 for α₁, etc. Tests establish the following:

| Case | Truthful grounded outcome | Truthful utilities (x,y,z) | Exact strategyproof? | Condition? |
|---|---|---|---|---|
| Example 5.10 | {a1,a3} | (1,0,1) | No | Fails |
| Example 5.11 | {a1,a4,a5,a6} | (4,0,0) | Yes | Fails |

In 5.10, hiding a1 yields {a2,a4,a5}, increasing x's utility from 1 to 2. The utilities follow the actual ownership, correcting the printed swap. In 5.11 the extra defender is a6, correcting the later reference to a5. The test checks all opponent subsets, rather than inferring dominance only from the truthful outcome.

Additional cases cover a defence chain, mutual attack, odd cycles, self-attacks, and the empty framework. In a mutual attack, complete extensions are ∅,{a},{b}; preferred, stable, and semi-stable extensions are {a},{b}. A directed triangle has grounded ∅ and no stable extensions.

## 5. Experimental design

The random generator uses Python's `random.Random(20261101)`. For each p and instance:

1. Draw n uniformly from {6,7,8}.
2. Include each ordered attack between distinct nodes independently with probability p. Reciprocal attacks and directed cycles are allowed. Self-attacks are excluded in the main experiment; `--self-attacks` enables them.
3. Assign every argument independently and uniformly to one of three agents, resampling the assignment until all agents are nonempty. Thus ownership is uniform over nonempty assignments conditional on n, not uniform over partition sizes.
4. Compute exact strategyproofness independently of the graph condition.
5. Record both booleans, graph, ownership, an odd-walk witness if present, and a profitable deviation if found.

`instances.jsonl` contains all 5,000 records. `summary.csv` is an aggregate; `metadata.json` records the settings and runtime. `case_studies.json` retains a representative instance of each observed category for every p, with explanatory statistics. Non-strategyproof witnesses are directly replayable.

## 6. Results

| p | Instances | Strategyproof fraction | Both pass | Condition passes, SP fails | SP passes, condition fails | Both fail |
|---|---:|---:|---:|---:|---:|---:|
| 0.1 | 1000 | 0.811 | 297 | 0 | 514 | 189 |
| 0.3 | 1000 | 0.181 | 14 | 0 | 167 | 819 |
| 0.5 | 1000 | 0.021 | 0 | 0 | 21 | 979 |
| 0.7 | 1000 | 0.007 | 0 | 0 | 7 | 993 |
| 0.9 | 1000 | 0.000 | 0 | 0 | 0 | 1000 |

There are **zero** instances satisfying the implemented sufficient condition yet failing exact strategyproofness. There are therefore no anomalous condition-passing instances to explain in this sample. This is experimental consistency, not a proof of the theorem.

There are **709** instances that are strategyproof although the condition fails. The condition detects possible internal conflict but does not measure the net accepted-argument gain from hiding. A direct internal attack may merely exchange which one of the agent's arguments is accepted, leaving utility unchanged. External defenders can also neutralize a potentially harmful chain. Cycles can produce additional conservative condition failures under the stated walk convention.

For a minimal analytical example, let one agent own {a,b}, another own {c}, and a→b be the only attack. Full revelation accepts a and gives the first agent utility 1. Hiding a may accept b but still gives utility 1. Hiding b retains a; hiding both gives 0. Opponents cannot change this because c is isolated. Thus truthfulness is weakly dominant while the condition fails. This explanation is a utility tie, not an assertion that internal attacks never matter.

Actual random examples, their graphs, and profile-wide maximum deviation gains are included in `case_studies.json` and discussed in `results/CASE_STUDIES.md`. For every retained strategyproof example, that maximum gain is 0 across all agents, reports, and opponent subsets. For a manipulable example it is positive. The exact enumeration is the definitive reason for each classification; structural explanations supplement it.

Strategyproofness becomes rarer over this particular density grid. Higher density creates more opportunities for selective revelation to break attack structures. This is an observed trend under this sampling model, not a general monotonicity theorem. With 1,000 independent instances per p, the worst-case binomial standard error is about 0.0158; a fraction of zero in the sample does not establish a population probability of zero.

## 7. Verification and complexity

The tests independently enumerate all 27 total labellings for every one of the 512 directed three-node graphs, including loops. They compare these with labellings produced from complete extensions, check grounded containment in every complete extension, and stable membership among preferred extensions. Dedicated tests cover the book outcomes, utility correction, strategic deviations, cycle termination, malformed endpoints, invalid ownership, and a UI API response.

Defence/characteristic calculations are polynomial. Grounded iteration adds at least one argument per nonterminal step, with at most n additions. Extension enumeration takes exponential time in n; preferred/semi-stable pairwise maximality filtering can cost O(4^n · n) beyond basic enumeration. Strategyproofness visits at most k·2^n own-report/opponent-profile combinations, with cached outcomes for at most 2^n unions. Each cached outcome requires a grounded computation on an induced graph. Odd-parity BFS over all sources costs O(n(n+m)). These are appropriate exact methods for 6–8 arguments; they are not intended for large frameworks.

The browser UI uses the same Python engine as the CLI. It supports editable attacks, sets, ownership, reports, all five semantics, acceptance tables, legal labellings, strategic witnesses, built-in book examples, CSV download, and JSON export. It has no external asset or runtime dependency.

## 8. Limitations and reproducibility

The p grid and self-attack convention are explicit choices because the assignment text omits them. Ownership is restricted to partitions as required by the random split; overlapping expertise is outside this submission. The graph certificate's walk convention is documented so a different classroom path convention can be identified. Experiments are finite evidence, while instance classifications are exhaustive. The UI limits graphs to 10 nodes to keep exhaustive interactive computations practical.

Reproduce with `python -m unittest -v`, `python demo.py`, and `python experiments.py`. The demonstration guide explains the visible workflow and expected results. The report is supplied as editable Markdown to allow adding student details and course formatting.

## References

1. Weiss, G. (ed.). *Multiagent Systems*, 2nd ed., MIT Press, 2013. [Publisher contents](https://mitpress.ublish.com/book/multiagent-systems-0).
2. Rahwan, I. “Argumentation Among Agents,” Chapter 5 in the above. [Author's publication list](https://web.mit.edu/~irahwan/www/publications.html); [institutional chapter metadata](https://www.mpib-berlin.mpg.de/staff/iyad-rahwan/publications?page=6).
3. [Search-indexed copy of the textbook](https://www.scribd.com/document/644752492/Multiagent-Systems-PDFDrive), used to identify the numbered examples and theorems; direct access may require the service's reader. The graph data are encoded in `book_examples.py` rather than reproducing textbook pages.
4. Rahwan, I., Larson, K., and Tohmé, F. “A Characterisation of Strategy-Proofness for Grounded Argumentation Semantics,” IJCAI 2009, pp. 251–255. [Proceedings](https://ijcai.org/proceedings/2009/51). Its background definitions support the formal model; its focal-argument preference results are not substituted for the assignment's count utility.
