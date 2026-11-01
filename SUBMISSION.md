# What to submit

Public repository: https://github.com/Aashcharya1/argumentation-engine

Submit the complete `argumentation-engine-submission.zip` from the parent folder, plus the public GitHub repository link if your course portal accepts one.

The ZIP contains:

- Code: `engine.py`, `book_examples.py`, `experiments.py`, `server.py`, `demo.py`, `test_engine.py`, and `web/index.html`.
- README: `README.md`, with setup, commands, API usage, and conventions.
- Report: `REPORT.md`, with definitions, algorithms, textbook examples, experiments, results, limitations, and references.
- Demonstration: `demo.py`, `DEMONSTRATION.md`, and actual output in `results/demo.txt`; `results/ui-preview.png` shows the UI.
- Experimental evidence: `results/summary.csv`, all 5,000 instances in `results/instances.jsonl`, metadata, case studies, and verification notes.
- Windows launcher: `START_UI.cmd`.

Before submitting, add your name, roll number, and any group members to the report if required. The assignment does not specify a report format; if the portal requires PDF, export the report to PDF first. If the instructor requires a demo video, record the walkthrough in `DEMONSTRATION.md`; the current package provides an executable demo and script, not a recorded video.

The probability grid is an explicit assumption because the supplied assignment omits p values. The implementation uses a documented odd-walk interpretation for cyclic indirect defeat. Review these assumptions against any classroom clarification.

For a live demonstration, run `python server.py` and open http://127.0.0.1:8000. Run `python -m unittest -v` to show the checks, then `python demo.py` for the textbook examples.
