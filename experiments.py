"""Reproducible random experiment; records every instance, not just aggregates."""
import argparse
import csv
import json
import random
import time
from pathlib import Path
from engine import ArgumentationFramework, GroundedMechanism, jsonable


def run(count=1000, probabilities=(.1, .3, .5, .7, .9), seed=20261101, self_attacks=False):
    rng = random.Random(seed)
    folder = Path(__file__).parent / 'results'
    folder.mkdir(exist_ok=True)
    summary = []
    started = time.perf_counter()
    with (folder / 'instances.jsonl').open('w', encoding='utf-8') as output:
        for p in probabilities:
            counts = {'both': 0, 'condition_only': 0, 'strategyproof_only': 0, 'neither': 0}
            for k in range(count):
                n = rng.randint(6, 8)
                args = [chr(97 + j) for j in range(n)]
                attacks = [(a, b) for a in args for b in args
                           if (self_attacks or a != b) and rng.random() < p]
                # Uniform independent assignment conditioned on all three agents nonempty.
                while True:
                    owners = [rng.randrange(3) for _ in args]
                    if len(set(owners)) == 3:
                        break
                ownership = [[a for a, owner in zip(args, owners) if owner == j] for j in range(3)]
                game = GroundedMechanism(ArgumentationFramework(args, attacks), ownership)
                sp, deviation = game.strategyproof()
                condition, path = game.odd_path_condition()
                group = ('both' if condition else 'strategyproof_only') if sp else ('condition_only' if condition else 'neither')
                counts[group] += 1
                record = dict(id=f'p{p}-{k:04}', p=p, arguments=args, attacks=attacks,
                              ownership=ownership, strategyproof=sp, condition=condition,
                              odd_walk=path, deviation=deviation, category=group)
                output.write(json.dumps(jsonable(record)) + '\n')
            row = dict(p=p, instances=count, strategyproof_fraction=(counts['both'] + counts['strategyproof_only']) / count, **counts)
            summary.append(row)
            print(row, flush=True)
    with (folder / 'summary.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    metadata = dict(seed=seed, per_probability=count, probabilities=probabilities,
                    self_attacks=self_attacks, agents=3, argument_counts=[6, 7, 8],
                    ownership='independent uniform, conditioned on nonempty agents',
                    runtime_seconds=round(time.perf_counter() - started, 3))
    (folder / 'metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=1000)
    parser.add_argument('--probabilities', type=float, nargs='+', default=[.1, .3, .5, .7, .9])
    parser.add_argument('--seed', type=int, default=20261101)
    parser.add_argument('--self-attacks', action='store_true')
    options = parser.parse_args()
    if options.count < 1 or any(not 0 <= p <= 1 for p in options.probabilities):
        parser.error('Positive count and probabilities in [0,1] required')
    run(options.count, options.probabilities, options.seed, options.self_attacks)
