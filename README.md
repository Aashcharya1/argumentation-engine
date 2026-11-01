# Argumentation Engine — Autonomous Systems E2E

A complete, dependency-free Python implementation of finite abstract argumentation, grounded strategic revelation, reproducible experiments, and a browser UI.

## Run

Requires Python 3.10 or newer; no pip packages, Node, database, or internet required.

From this folder:

```powershell
python server.py
```

Open http://127.0.0.1:8000 in a browser. Stop with Ctrl+C. Use `python server.py --port 8001` if port 8000 is occupied. Windows users can also double-click `START_UI.cmd`.

```powershell
python -m unittest -v
python demo.py
python experiments.py
```

The experiment command reproduces the supplied 5,000 records (1,000 per probability). Optional overrides:

```powershell
python experiments.py --count 1000 --probabilities 0.1 0.3 0.5 0.7 0.9 --seed 20261101
python experiments.py --self-attacks
```

Experiment reruns replace the result files; the second command changes the graph distribution.

## Files

| File | Purpose |
|---|---|
| `engine.py` | Framework, semantics, legal labellings, acceptance, mechanisms |
| `book_examples.py` | Textbook Examples 5.10 and 5.11, with corrected utilities |
| `server.py`, `web/index.html` | Local API and interactive graph UI |
| `test_engine.py` | Unit tests and independent exhaustive labelling oracle |
| `experiments.py` | Seeded generator and exact experiment runner |
| `demo.py`, `DEMONSTRATION.md` | Executable demo and presentation walkthrough |
| `REPORT.md` | Methods, results, interpretation, assumptions, references |
| `results/summary.csv` | Results grouped by attack probability |
| `results/instances.jsonl` | Every graph, partition, classification, and witness |
| `results/metadata.json` | Seed, distribution, and measured runtime |
| `results/case_studies.json` | Representative actual random instances |
| `results/demo.txt` | Captured demonstration output |

## API example

```python
from engine import ArgumentationFramework, GroundedMechanism

af = ArgumentationFramework(['a', 'b', 'c'], [('a', 'b'), ('b', 'c')])
assert af.conflict_free({'a', 'c'})
assert af.defends({'a'}, 'c')
assert af.characteristic(set()) == {'a'}
assert af.admissible({'a'})
assert af.complete({'a', 'c'})
assert af.grounded_extension() == {'a', 'c'}
print(af.complete_extensions())
print(af.preferred_extensions())
print(af.stable_extensions())
print(af.semi_stable_extensions())
print(af.legal_labellings())
print(af.acceptance_status('a', 'preferred'))

game = GroundedMechanism(af, [{'a'}, {'b'}, {'c'}])
print(game.outcome([{'a'}, {'b'}, {'c'}]))
print(game.best_responses(0, game.ownership))
print(game.strategyproof())       # exact Theorem 5.3 check, with deviation witness
print(game.odd_path_condition())  # sufficient Theorem 5.4 condition, with odd walk
```

Extensions are frozensets; extension families are lists. `jsonable` converts them for JSON. `best_responses` returns `(maximum_utility, all_maximising_reports)`. A strategyproof result is `(True, None)` or `(False, deviation)`. Odd-path results are `(condition_holds, violating_walk_or_None)`.

## Input and conventions

- Attack `(a,b)` means a attacks b. Argument names are strings.
- All extensions and best responses are exact, without random search.
- Preferred and semi-stable maximality use set inclusion, not largest cardinality.
- The phrase “semi semi-stable” is interpreted as semi-stable semantics.
- Utility is the number of the agent's own accepted arguments.
- Ownership is a disjoint partition, matching the random-split assignment; empty agents are supported by the library. Experiments condition on three nonempty agents.
- Stable acceptance with no stable extensions is explicitly undefined, avoiding vacuous skeptical acceptance.
- “Rejected” means accepted in no extension; it does not imply labelled out in every labelling.
- Odd reachability includes positive odd closed walks and repeated vertices. See the report for cycle handling and the distinction from simple paths.
- Interactive exhaustive analysis is capped at 10 arguments; the Python library has no artificial cap but is exponential.
- Book identified as Weiss (ed.), *Multiagent Systems*, second edition (2013), Chapter 5. The assignment omits p values, so the chosen grid is an explicit assumption.
