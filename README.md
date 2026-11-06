# Argumentation Engine and Strategic Revelation

**Autonomous Systems (CSL7650) · Assignment 3**

| Submitted by | Roll number |
|---|---|
| Aashcharya Gorakh | B23ES1001 |
| Damarasingu Akshaya Sree | B23EE1085 |

A self-contained Python implementation of finite abstract argumentation and strategic argument revelation. The project computes exact argumentation semantics, determines whether agents can benefit by hiding arguments under a grounded mechanism, and compares exhaustive strategyproofness checks with a sufficient graph condition over **5,000 reproducible random instances**.

The submission includes a local browser interface, textbook regression examples, automated verification, complete experimental records, and a technical report. Application code uses only the Python standard library and browser-native HTML, CSS, and JavaScript.

## Submission guide

| Material | Purpose |
|---|---|
| [Technical report (PDF)](Argumentation_engine.pdf) | Formal definitions, algorithms, figures, experimental analysis, limitations, and references |
| [Demonstration guide](DEMONSTRATION.md) | Approximately six-minute walkthrough with expected outcomes |
| [Engine](engine.py) and [tests](test_engine.py) | Implementation and executable correctness checks |
| [Experimental summary](results/summary.csv) | Results grouped by attack probability |
| [Full dataset](results/instances.jsonl) | Every framework, ownership partition, classification, and available witness |
| [Case studies](results/CASE_STUDIES.md) | Explanations of representative generated instances |

For assessment, start the UI, run the tests and demonstration, then inspect the report and saved experiment artifacts. The original marking rubric is not included in this repository; the coverage table below identifies implemented capabilities and their evidence.

## Quick start

### Requirements

- **Python 3.10 or newer**, available in your terminal.
- A modern browser for the optional graphical interface.
- No third-party Python packages, Node.js, database, API keys, or internet connection are required to run locally.

Open a terminal in the project folder containing `server.py` and `engine.py`:

```powershell
python --version
python server.py
```

Open **http://127.0.0.1:8000**. Keep the terminal running while using the application; press **Ctrl+C** to stop it. Windows users can also double-click [START_UI.cmd](START_UI.cmd).

If port 8000 is occupied:

```powershell
python server.py --port 8001
```

Then open http://127.0.0.1:8001. Where Python is named `python3`, substitute `python3` in these commands. Windows users can use `py -3` if it launches their Python 3.10+ installation.

### Verify and demonstrate

In a separate terminal, from the project folder:

```powershell
python -m unittest -v
python demo.py
```

The suite contains **eight tests**, including exhaustive checks across all **512 directed three-argument graphs**, with self-attacks allowed. A successful run ends with `OK`. The demo prints all five semantics for mutual attack and the outcomes, utilities, best responses, and strategic classifications of both textbook examples.

The supplied experimental results can be reviewed immediately; rerunning experiments is optional.

## Implemented capabilities and evidence

| Capability | Implementation | Evidence / demonstration |
|---|---|---|
| Framework construction and validation | `ArgumentationFramework` | Unknown endpoints and invalid sets rejected; empty frameworks supported |
| Conflict-freeness, defence, characteristic function | `conflict_free`, `defends`, `characteristic` | Defence-chain example and tests |
| Admissibility and completeness | `admissible`, `complete` | Editable test set S in the UI |
| Grounded, complete, preferred, stable, semi-stable semantics | Extension methods in `engine.py` | UI selector, demo, and regression tests |
| All legal total labellings | `legal_labellings` | Independent oracle across all 512 three-node graphs |
| Skeptical / credulous acceptance and rejection | `acceptance_status` | Acceptance table for each semantics |
| Grounded mechanism for partial revelation | `GroundedMechanism.outcome` | Editable ownership and reports |
| Count utility and all optimal reports | `utility`, `best_responses` | Profitable-hiding example |
| Exact dominant-strategy truthfulness | `strategyproof` | All opponents' profiles checked; profitable-deviation witness on failure |
| Sufficient condition associated with Theorem 5.4 | `odd_path_condition` | Cycle-safe parity search with odd-walk witness |
| Textbook strategic examples | `book_examples.py` | Examples 5.10 and 5.11, tested and demonstrated |
| Random experiments and interpretation | `experiments.py`, `results/`, report | 1,000 instances at each of five attack probabilities |

## Using the browser interface

1. Select a built-in example: **Defence chain**, **Mutual attack**, **Odd cycle**, **Profitable hiding**, or **Protective defender**, among others.
2. Edit arguments, attacks, ownership, revealed reports, or test set S.
3. Click **Analyse framework** and choose a semantics to inspect its extensions and acceptance table.
4. Inspect strategic outcomes, utilities, exact strategyproofness, and the graph condition. Expand **Best reports and odd-walk witness** for details.
5. Use **Export JSON** under **Full analysis JSON** to save the analysis, or **Download results CSV** for the saved summary.

### Input format

| Field | Format | Example |
|---|---|---|
| Arguments | Comma-separated names | `a,b,c` |
| Attacks | One `source,target` pair per line | `a,b` followed by `b,c` on the next line |
| Ownership | One agent per line; comma-separated owned arguments | Lines `a`, `b`, `c` define three agents |
| Reports | One line per agent in ownership order | A blank line means that agent hides everything |
| Test set S | Comma-separated names; empty means the empty set | `a,c` |

Attack `(a,b)` means **a attacks b**. Ownership must partition all arguments: each argument belongs to exactly one agent. Reports must be subsets of the corresponding ownership sets. Agent indices start at **0**. Empty agents are supported by the library and UI; the main experiments require three nonempty agents.

The semantics and set-analysis panels evaluate the full entered framework. The strategic outcome evaluates the subframework induced by revealed arguments and always uses **grounded semantics**. Changing the semantics selector changes the extension display and acceptance table. Graph colours show the **first extension** of the selected family; consult the extension table for alternatives. Legal labellings list all complete labellings independently of the selector.

Interactive analysis supports at most **10 arguments** because computations are exhaustive. Use the server URL: opening `web/index.html` directly does not start its Python API.

## Formal model and algorithms

An argumentation framework is **AF = (A, R)**, with finite arguments A and directed attacks R. For S contained in A, let **S+** be the arguments attacked by S, and let **F(S)** be the arguments whose attackers are all attacked by S.

| Concept | Definition used |
|---|---|
| Conflict-free | S contains no internal attack |
| Defence of a by S | S attacks every attacker of a |
| Admissible | S is conflict-free and contained in F(S) |
| Complete | S is conflict-free and S = F(S) |
| Grounded | Least fixed point of F, iterated from the empty set |
| Preferred | Inclusion-maximal admissible sets |
| Stable | Conflict-free sets with range S union S+ equal to A |
| Semi-stable | Complete extensions with inclusion-maximal range |

Maximality uses **set inclusion**, rather than maximum cardinality. Other than grounded fixed-point iteration, extension families use exact subset enumeration.

Each complete extension E produces a legal total labelling: E is `in`, arguments attacked by E are `out`, and the remainder are `undec`. This correspondence generates all legal labellings.

Acceptance is relative to a semantics. The API returns `skeptically accepted` for membership in every extension, `credulously accepted` for membership in some but not all, and `rejected` for membership in none. With no extensions, it returns `undefined (no extensions)`. A rejected argument can still be undecided: rejection concerns extension membership rather than universal `out` labelling.

### Strategic revelation

Agent i owns A_i and reports any subset R_i, including the empty set. The mechanism returns the grounded extension of the graph induced by the union of reports. Hidden arguments and their incident attacks disappear. Utility counts the agent's **own accepted arguments**:

```text
u_i(R_i, R_-i) = |A_i intersect Grounded(AF[union of reports])|
```

`best_responses` returns maximum utility and every report attaining it against fixed opponents' reports. The exact strategyproofness test checks:

```text
For every agent i, every opponents' report profile R_-i,
and every alternative report T_i contained in A_i:

u_i(A_i, R_-i) >= u_i(T_i, R_-i)
```

Truthfulness must therefore be **weakly dominant**, including when opponents hide arguments. Ties are allowed. A failure returns a concrete agent, report profile, truthful utility, best utility, and all best reports for that profile. Outcomes are cached by the revealed union.

### Sufficient condition and cycles

The separate graph test checks for the absence of positive odd directed walks between arguments belonging to the same agent. Breadth-first search over `(argument, parity)` states terminates even with cycles. Repeated vertices and positive odd returns to the starting argument count.

This is a **conservative walk-based interpretation** of the condition associated with Theorem 5.4. A simple-path convention differs on cyclic graphs. Passing the condition is a sufficient certificate; failing it does **not** establish manipulability. Exact strategyproofness is computed independently and is unaffected by this convention.

## Textbook examples and expected outcomes

The strategic cases follow Chapter 5, “Argumentation Among Agents,” in Gerhard Weiss (ed.), *Multiagent Systems*, second edition (2013). Code names `a1`, `a2`, etc. denote the book's alpha-indexed arguments.

| Example / UI name | Truthful grounded outcome | Utilities (x,y,z) | Strategyproof? | Condition |
|---|---|---|---|---|
| 5.10 / Profitable hiding | `{a1,a3}` | `(1,0,1)` | No | Fails |
| 5.11 / Protective defender | `{a1,a4,a5,a6}` | `(4,0,0)` | Yes | Fails |

In Example 5.10, x owns `{a1,a4,a5}`, y owns `{a2}`, and z owns `{a3}`. Change x's report to `a4,a5`, leaving other reports unchanged. The outcome becomes `{a2,a4,a5}` and x's utility rises from **1 to 2**. In Example 5.11, x also owns a6, which attacks a3; exhaustive checking establishes strategyproofness despite failure of the condition.

Utilities follow actual ownership, correcting the printed swap in Example 5.10. The protective defender in Example 5.11 is a6; the later a5 reference is treated as a misprint. The report explains these choices. The project reproduces these two strategic cases and additional semantic examples, rather than every figure in the chapter.

## Reproducible experiments

### Sampling protocol

The supplied run uses seed **20261101**, three agents, and **1,000 instances per probability** for p in `{0.1,0.3,0.5,0.7,0.9}`. For each instance:

1. Draw n uniformly from `{6,7,8}`.
2. Include every ordered attack between distinct arguments independently with probability p. Reciprocal attacks and cycles are allowed; self-attacks are excluded by default.
3. Assign arguments independently and uniformly to three agents, resampling ownership until all agents are nonempty. Ownership-set sizes are not sampled uniformly.
4. Independently compute exact strategyproofness and the condition, retaining classifications and available witnesses.

The report records that the assignment's probability values were missing; the five-point grid is an explicit assumption. “Semi semi-stable” is interpreted as semi-stable semantics.

### Reproduction commands

```powershell
python experiments.py
```

Equivalent explicit configuration:

```powershell
python experiments.py --count 1000 --probabilities 0.1 0.3 0.5 0.7 0.9 --seed 20261101
```

`--count` is the number of instances **per probability**. Optional examples:

```powershell
python experiments.py --count 20 --probabilities 0.1 0.5 --seed 42
python experiments.py --self-attacks
```

**Reruns overwrite `results/instances.jsonl`, `results/summary.csv`, and `results/metadata.json`.** Copy the baseline files first if you want to retain them. Alternative settings change the dataset and the UI CSV download. The runner does not regenerate curated case studies, saved verification notes, the demonstration transcript, report tables, or PDF; those describe the supplied baseline. Runtime depends on the machine; witness ordering can differ even when classifications agree.

### Supplied results

SP denotes exact strategyproofness; C denotes the implemented odd-walk condition.

| p | Instances | SP fraction | SP and C | C, not SP | SP, not C | Neither |
|---|---:|---:|---:|---:|---:|---:|
| 0.1 | 1,000 | 0.811 | 297 | 0 | 514 | 189 |
| 0.3 | 1,000 | 0.181 | 14 | 0 | 167 | 819 |
| 0.5 | 1,000 | 0.021 | 0 | 0 | 21 | 979 |
| 0.7 | 1,000 | 0.007 | 0 | 0 | 7 | 993 |
| 0.9 | 1,000 | 0.000 | 0 | 0 | 0 | 1,000 |
| **Total** | **5,000** | **0.204** | **311** | **0** | **709** | **3,980** |

No sampled instance passes the condition while failing the strategic test. This is finite evidence consistent with sufficiency, rather than a proof. **709 instances are strategyproof despite failing the condition**, showing the certificate is not necessary in this sample.

Internal attacks may exchange one accepted owned argument for another without increasing utility, while external defenders may neutralise harmful chains. See the [actual case studies](results/CASE_STUDIES.md). Strategyproofness decreases across this sampled density grid; this is an observed trend under the stated distribution, rather than a general monotonicity theorem. Zero observed strategyproof instances at p = 0.9 does not imply zero population probability.

### Experimental artifacts

| File in `results/` | Contents |
|---|---|
| `summary.csv` | Per-probability counts and fractions; categories `both`, `condition_only`, `strategyproof_only`, `neither` |
| `instances.jsonl` | One JSON object per instance: ID, p, graph, ownership, booleans, category, and available odd-walk / profitable-deviation witnesses |
| `metadata.json` | Seed, sample counts, probabilities, self-attack setting, ownership distribution, measured runtime |
| `case_studies.json` | Curated baseline examples and profile-wide deviation-gain analysis |
| `CASE_STUDIES.md` | Human-readable interpretation of curated examples |

## Python library usage

Run from the project folder, or save this as a Python file alongside `engine.py`:

```python
from engine import ArgumentationFramework, GroundedMechanism, jsonable

af = ArgumentationFramework(
    ["a", "b", "c"],
    [("a", "b"), ("b", "c")],
)
assert af.conflict_free({"a", "c"})
assert af.defends({"a"}, "c")
assert af.characteristic(set()) == {"a"}
assert af.admissible({"a"})
assert not af.complete({"a"})
assert af.grounded_extension() == {"a", "c"}

for semantics in ("grounded", "complete", "preferred", "stable", "semi-stable"):
    print(semantics, jsonable(af.extensions(semantics)))

print(af.legal_labellings())
print(af.acceptance_status("a", "preferred"))

game = GroundedMechanism(af, [{"a"}, {"b"}, {"c"}])
assert game.outcome(game.ownership) == {"a", "c"}
print(game.best_responses(0, game.ownership))
print(game.strategyproof())
print(game.odd_path_condition())
```

Extensions are `frozenset` objects; extension families are lists. `jsonable` converts nested results into JSON-compatible structures. `best_responses` returns `(maximum_utility, all_maximising_reports)`. Strategyproofness returns `(True, None)` or `(False, deviation)`. Condition checks return `(condition_holds, violating_walk_or_None)`.

## Local HTTP API

The server binds to `127.0.0.1`. Routes are `GET /` for the UI, `GET /results` for the saved CSV, and `POST /api/analyse` for JSON analysis.

Example request body:

```json
{
  "arguments": ["a", "b", "c"],
  "attacks": [["a", "b"], ["b", "c"]],
  "set": ["a"],
  "ownership": [["a"], ["b"], ["c"]],
  "reports": [["a"], ["b"], ["c"]]
}
```

Responses contain `extensions`, `labellings`, `set_analysis`, and `acceptance`, plus `strategic` when ownership is supplied. `set` defaults to empty; reports default to full ownership. Without ownership, only semantic analysis is returned. Handled validation errors produce HTTP 400 with an `error` message. Request bodies are limited to 100,000 bytes and frameworks to 10 arguments.

## Verification and computational limits

The tests cover textbook outcomes, chains, mutual attacks, odd cycles, self-attacks, empty frameworks, invalid endpoints and ownership, parity traversal, and a direct call to the server analysis function. The independent oracle evaluates all **27 total labellings for each of 512 three-node graphs**, comparing local legality with the engine's complete-extension labellings. It also checks grounded containment in every complete extension and stable membership among preferred extensions.

Grounded iteration and basic defence operations are polynomial. Extension enumeration is exponential; pairwise inclusion filtering can introduce a `4^n` factor. Exact strategic enumeration visits up to `k * 2^n` report combinations, caching outcomes for at most `2^n` revealed unions. Odd-walk detection costs `O(n(n + m))`, for n arguments and m attacks. These exact methods target small frameworks, particularly the experiment's 6–8 arguments. The Python library has no artificial size cap, but exhaustive analyses can be expensive.

The model assumes disjoint ownership, hiding-only reports, and count utility. Overlapping ownership, fabricated arguments, alternative preferences, and other dialogue protocols are outside scope.

## Repository layout

```text
argumentation-engine/
|-- README.md                 # Setup, usage, and submission overview
|-- Argumentation_engine.pdf  # Formatted technical report
|-- DEMONSTRATION.md          # Presentation walkthrough
|-- engine.py                 # Semantics and strategic mechanism
|-- book_examples.py          # Textbook Examples 5.10 and 5.11
|-- test_engine.py            # Tests and independent labelling oracle
|-- demo.py                   # Executable demonstration
|-- experiments.py            # Seeded experiment runner
|-- server.py                 # Local server and analysis API
|-- START_UI.cmd              # Windows launcher
|-- web/
|   `-- index.html            # Interface and graph visualisation
`-- results/
    |-- summary.csv
    |-- instances.jsonl
    |-- metadata.json
    |-- case_studies.json
    |-- CASE_STUDIES.md
    |-- demo.txt              # Saved demonstration output
    |-- verification.txt      # Saved verification notes
    `-- ui-preview.png        # Saved interface preview
```

## Troubleshooting

| Problem | Resolution |
|---|---|
| Python command is unavailable | Install Python 3.10+ with PATH enabled, or use a working `py -3` / `python3` command |
| `server.py` cannot be found | Change into the project folder |
| Address already in use | Use `--port 8001` and open the matching URL |
| Browser cannot connect | Keep the server running and use its printed HTTP URL |
| Unknown endpoint / invalid set | Use declared argument names throughout |
| Ownership or report error | Assign every argument exactly once; keep one report per agent, contained in its ownership |
| No stable extensions | A valid result, for example on an odd cycle; stable acceptance is undefined |
| Interactive size-limit error | Reduce the framework to at most 10 arguments |

## References

1. Dung, P. M. (1995). *On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games.* Artificial Intelligence, 77(2), 321–357. DOI: `10.1016/0004-3702(94)00041-X`.
2. Weiss, G. (ed.) (2013). *Multiagent Systems*, second edition. MIT Press. Chapter 5, “Argumentation Among Agents,” by Iyad Rahwan, pp. 177–210. Source for the numbered strategic examples and theorem discussion.
3. Rahwan, I., Larson, K., and Tohmé, F. (2009). *A Characterisation of Strategy-Proofness for Grounded Argumentation Semantics.* IJCAI, pp. 251–255. Background reference; its focal-argument preferences are not substituted for this project's count utility.

See the technical report for source links, detailed interpretation, and textbook corrections.
