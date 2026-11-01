# Actual random-instance case studies

These graphs are selected from the saved random run, one per observed category and probability. Reports use agent indices starting at 0. A maximum deviation gain of zero verifies that hiding never improves utility in any opponent profile.

## p0.1-0000 — strategyproof_only

Ownership: [['b', 'c'], ['e', 'f'], ['a', 'd', 'g', 'h']]
Attacks: [['a', 'b'], ['a', 'd'], ['a', 'e'], ['c', 'd'], ['e', 'd'], ['e', 'f']]
Truthful outcome: ['a', 'c', 'f', 'g', 'h']
Odd-walk witness: ['e', 'f']
Maximum deviation gain across all profiles: 0.

The odd walk exposes an internal conflict, but exhaustive utility comparison finds no strict gain. Acceptance changes can be utility ties or losses; the witness alone is insufficient to establish manipulation.

## p0.1-0001 — neither

Ownership: [['a'], ['f'], ['b', 'c', 'd', 'e', 'g']]
Attacks: [['a', 'd'], ['b', 'a'], ['c', 'a'], ['d', 'g'], ['e', 'c'], ['g', 'd']]
Truthful outcome: ['b', 'e', 'f']
Odd-walk witness: ['b', 'a', 'd', 'g']
Maximum deviation gain across all profiles: 1.

Profitable deviation (replayable):
```json
{
  "agent": 2,
  "others_profile": [
    [],
    [],
    [
      "b",
      "c",
      "d",
      "e",
      "g"
    ]
  ],
  "truthful_utility": 2,
  "best_utility": 3,
  "best_reports": [
    [
      "b",
      "c",
      "d"
    ],
    [
      "b",
      "d",
      "e"
    ],
    [
      "b",
      "c",
      "d",
      "e"
    ],
    [
      "b",
      "c",
      "g"
    ],
    [
      "b",
      "e",
      "g"
    ],
    [
      "b",
      "c",
      "e",
      "g"
    ]
  ]
}
```

## p0.1-0003 — both

Ownership: [['a', 'd', 'e'], ['f'], ['b', 'c']]
Attacks: [['b', 'e'], ['b', 'f']]
Truthful outcome: ['a', 'b', 'c', 'd']
Odd-walk witness: None
Maximum deviation gain across all profiles: 0.

## p0.3-0000 — neither

Ownership: [['c', 'd', 'f', 'g'], ['e'], ['a', 'b']]
Attacks: [['a', 'd'], ['b', 'a'], ['c', 'e'], ['d', 'a'], ['d', 'b'], ['d', 'e'], ['e', 'b'], ['e', 'c'], ['e', 'd'], ['e', 'f'], ['f', 'd'], ['f', 'e'], ['g', 'a'], ['g', 'f']]
Truthful outcome: ['g']
Odd-walk witness: ['c', 'e', 'f', 'd']
Maximum deviation gain across all profiles: 1.

Profitable deviation (replayable):
```json
{
  "agent": 2,
  "others_profile": [
    [
      "c"
    ],
    [
      "e"
    ],
    [
      "a",
      "b"
    ]
  ],
  "truthful_utility": 0,
  "best_utility": 1,
  "best_reports": [
    [
      "a"
    ]
  ]
}
```

## p0.3-0003 — strategyproof_only

Ownership: [['b', 'd', 'f'], ['a', 'c'], ['e', 'g']]
Attacks: [['a', 'c'], ['b', 'f'], ['c', 'b'], ['c', 'd'], ['c', 'e'], ['c', 'g'], ['e', 'b'], ['g', 'b'], ['g', 'e']]
Truthful outcome: ['a', 'd', 'f', 'g']
Odd-walk witness: ['b', 'f']
Maximum deviation gain across all profiles: 0.

The odd walk exposes an internal conflict, but exhaustive utility comparison finds no strict gain. Acceptance changes can be utility ties or losses; the witness alone is insufficient to establish manipulation.

## p0.3-0068 — both

Ownership: [['f'], ['a', 'b', 'd'], ['c', 'e', 'g']]
Attacks: [['a', 'e'], ['a', 'g'], ['b', 'c'], ['b', 'e'], ['c', 'f'], ['e', 'd'], ['f', 'e'], ['f', 'g'], ['g', 'd']]
Truthful outcome: ['a', 'b', 'd', 'f']
Odd-walk witness: None
Maximum deviation gain across all profiles: 0.

## p0.5-0000 — neither

Ownership: [['a', 'g'], ['b', 'd', 'f', 'h'], ['c', 'e']]
Attacks: [['a', 'c'], ['a', 'd'], ['a', 'e'], ['a', 'f'], ['b', 'a'], ['b', 'd'], ['c', 'a'], ['c', 'b'], ['c', 'd'], ['c', 'f'], ['c', 'h'], ['d', 'a'], ['d', 'c'], ['d', 'e'], ['d', 'g'], ['e', 'b'], ['e', 'd'], ['e', 'f'], ['e', 'g'], ['e', 'h'], ['f', 'a'], ['f', 'c'], ['f', 'd'], ['f', 'g'], ['f', 'h'], ['g', 'a'], ['g', 'b'], ['g', 'c'], ['h', 'b'], ['h', 'g']]
Truthful outcome: []
Odd-walk witness: ['a', 'c', 'b', 'a']
Maximum deviation gain across all profiles: 2.

Profitable deviation (replayable):
```json
{
  "agent": 0,
  "others_profile": [
    [
      "a",
      "g"
    ],
    [],
    [
      "e"
    ]
  ],
  "truthful_utility": 0,
  "best_utility": 1,
  "best_reports": [
    [
      "a"
    ]
  ]
}
```

## p0.5-0011 — strategyproof_only

Ownership: [['e'], ['c', 'd', 'f'], ['a', 'b']]
Attacks: [['b', 'c'], ['b', 'd'], ['b', 'e'], ['c', 'b'], ['c', 'e'], ['d', 'a'], ['d', 'c'], ['d', 'e'], ['e', 'b'], ['e', 'c'], ['e', 'd'], ['e', 'f'], ['f', 'd'], ['f', 'e']]
Truthful outcome: []
Odd-walk witness: ['e', 'b', 'c', 'e']
Maximum deviation gain across all profiles: 0.

The odd walk exposes an internal conflict, but exhaustive utility comparison finds no strict gain. Acceptance changes can be utility ties or losses; the witness alone is insufficient to establish manipulation.

## p0.7-0000 — neither

Ownership: [['b', 'c', 'd'], ['a', 'g'], ['e', 'f']]
Attacks: [['a', 'b'], ['a', 'd'], ['a', 'e'], ['a', 'g'], ['b', 'a'], ['b', 'c'], ['b', 'd'], ['b', 'e'], ['b', 'f'], ['b', 'g'], ['c', 'd'], ['c', 'f'], ['c', 'g'], ['d', 'b'], ['d', 'c'], ['d', 'e'], ['d', 'g'], ['e', 'b'], ['e', 'c'], ['e', 'd'], ['e', 'f'], ['e', 'g'], ['f', 'a'], ['f', 'b'], ['f', 'd'], ['f', 'e'], ['g', 'a'], ['g', 'b'], ['g', 'e']]
Truthful outcome: []
Odd-walk witness: ['b', 'c']
Maximum deviation gain across all profiles: 1.

Profitable deviation (replayable):
```json
{
  "agent": 0,
  "others_profile": [
    [
      "b",
      "c",
      "d"
    ],
    [],
    []
  ],
  "truthful_utility": 0,
  "best_utility": 1,
  "best_reports": [
    [
      "b"
    ],
    [
      "c"
    ],
    [
      "b",
      "c"
    ],
    [
      "d"
    ]
  ]
}
```

## p0.7-0011 — strategyproof_only

Ownership: [['a'], ['b', 'd'], ['c', 'e', 'f']]
Attacks: [['a', 'b'], ['a', 'e'], ['a', 'f'], ['b', 'a'], ['b', 'e'], ['c', 'a'], ['c', 'b'], ['c', 'd'], ['c', 'e'], ['c', 'f'], ['d', 'a'], ['d', 'b'], ['d', 'c'], ['d', 'e'], ['d', 'f'], ['e', 'a'], ['e', 'b'], ['e', 'd'], ['e', 'f'], ['f', 'a'], ['f', 'b'], ['f', 'd']]
Truthful outcome: []
Odd-walk witness: ['a', 'b', 'e', 'a']
Maximum deviation gain across all profiles: 0.

The odd walk exposes an internal conflict, but exhaustive utility comparison finds no strict gain. Acceptance changes can be utility ties or losses; the witness alone is insufficient to establish manipulation.

## p0.9-0000 — neither

Ownership: [['a', 'c'], ['b', 'd', 'e', 'f'], ['g']]
Attacks: [['a', 'b'], ['a', 'c'], ['a', 'd'], ['a', 'e'], ['a', 'f'], ['a', 'g'], ['b', 'a'], ['b', 'd'], ['b', 'f'], ['b', 'g'], ['c', 'a'], ['c', 'b'], ['c', 'd'], ['c', 'f'], ['d', 'a'], ['d', 'b'], ['d', 'c'], ['d', 'e'], ['d', 'f'], ['d', 'g'], ['e', 'a'], ['e', 'b'], ['e', 'c'], ['e', 'd'], ['e', 'f'], ['e', 'g'], ['f', 'a'], ['f', 'b'], ['f', 'c'], ['f', 'd'], ['f', 'g'], ['g', 'a'], ['g', 'b'], ['g', 'c'], ['g', 'd'], ['g', 'e'], ['g', 'f']]
Truthful outcome: []
Odd-walk witness: ['a', 'c']
Maximum deviation gain across all profiles: 1.

Profitable deviation (replayable):
```json
{
  "agent": 0,
  "others_profile": [
    [
      "a",
      "c"
    ],
    [],
    []
  ],
  "truthful_utility": 0,
  "best_utility": 1,
  "best_reports": [
    [
      "a"
    ],
    [
      "c"
    ]
  ]
}
```
