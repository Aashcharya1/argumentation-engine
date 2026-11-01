"""Finite Dung argumentation and exhaustive strategic analysis (standard library only)."""
from collections import deque
from itertools import product


def subsets(items):
    items = tuple(sorted(items))
    return [frozenset(x for j, x in enumerate(items) if m & (1 << j))
            for m in range(1 << len(items))]


class ArgumentationFramework:
    def __init__(self, arguments, attacks):
        self.arguments = frozenset(arguments)
        if any(not isinstance(a, str) for a in self.arguments):
            raise ValueError('Argument names must be strings')
        self.attacks = frozenset(tuple(e) for e in attacks)
        if any(len(e) != 2 or not set(e) <= self.arguments for e in self.attacks):
            raise ValueError('Each attack must have two known endpoints')
        self.attackers = {a: frozenset(x for x, y in self.attacks if y == a)
                          for a in self.arguments}

    def _set(self, s):
        s = frozenset(s)
        if not s <= self.arguments:
            raise ValueError('Unknown argument in set')
        return s

    def attacked(self, s):
        s = self._set(s)
        return frozenset(y for x, y in self.attacks if x in s)

    def conflict_free(self, s):
        s = self._set(s)
        return not bool(s & self.attacked(s))

    def defends(self, s, argument):
        if argument not in self.arguments:
            raise ValueError('Unknown argument')
        return self.attackers[argument] <= self.attacked(s)

    def characteristic(self, s):
        attacked = self.attacked(s)
        return frozenset(a for a in self.arguments if self.attackers[a] <= attacked)

    def admissible(self, s):
        s = self._set(s)
        return self.conflict_free(s) and s <= self.characteristic(s)

    def complete(self, s):
        s = self._set(s)
        return self.conflict_free(s) and s == self.characteristic(s)

    def induced(self, s):
        s = self._set(s)
        return ArgumentationFramework(s, [(x, y) for x, y in self.attacks if x in s and y in s])

    def grounded_extension(self):
        s = frozenset()
        while True:
            nxt = self.characteristic(s)
            if nxt == s:
                return s
            s = nxt

    def complete_extensions(self):
        return [s for s in subsets(self.arguments) if self.complete(s)]

    def preferred_extensions(self):
        candidates = [s for s in subsets(self.arguments) if self.admissible(s)]
        return [s for s in candidates if not any(s < t for t in candidates)]

    def stable_extensions(self):
        return [s for s in subsets(self.arguments)
                if self.conflict_free(s) and s | self.attacked(s) == self.arguments]

    def semi_stable_extensions(self):
        candidates = self.complete_extensions()
        ranges = {s: s | self.attacked(s) for s in candidates}
        return [s for s in candidates if not any(ranges[s] < ranges[t] for t in candidates)]

    def legal_labellings(self):
        # Complete extensions and total legal labellings are in bijection.
        return [{a: 'in' if a in s else 'out' if a in self.attacked(s) else 'undec'
                 for a in sorted(self.arguments)} for s in self.complete_extensions()]

    def acceptance_status(self, argument, semantics='grounded'):
        if argument not in self.arguments:
            raise ValueError('Unknown argument')
        extensions = self.extensions(semantics)
        if not extensions:
            return 'undefined (no extensions)'
        if all(argument in s for s in extensions):
            return 'skeptically accepted'
        if any(argument in s for s in extensions):
            return 'credulously accepted'
        return 'rejected'

    def extensions(self, semantics):
        methods = {'grounded': lambda: [self.grounded_extension()],
                   'complete': self.complete_extensions, 'preferred': self.preferred_extensions,
                   'stable': self.stable_extensions, 'semi-stable': self.semi_stable_extensions}
        if semantics not in methods:
            raise ValueError('Unknown semantics')
        return methods[semantics]()


class GroundedMechanism:
    def __init__(self, framework, ownership):
        self.framework = framework
        self.ownership = tuple(framework._set(s) for s in ownership)
        union = frozenset().union(*self.ownership)
        if union != framework.arguments or sum(map(len, self.ownership)) != len(union):
            raise ValueError('Ownership must partition all arguments')
        self._cache = {}

    def outcome(self, reports):
        reports = tuple(frozenset(s) for s in reports)
        if len(reports) != len(self.ownership) or any(not s <= own for s, own in zip(reports, self.ownership)):
            raise ValueError('One truthful-subset report per agent is required')
        union = frozenset().union(*reports)
        if union not in self._cache:
            self._cache[union] = self.framework.induced(union).grounded_extension()
        return self._cache[union]

    def utility(self, agent, reports):
        # Utility counts accepted OWN arguments, not all accepted arguments.
        return len(self.ownership[agent] & self.outcome(reports))

    def best_responses(self, agent, reports):
        self.outcome(reports)  # validate even the agent's current report
        trials = []
        for s in subsets(self.ownership[agent]):
            trial = list(reports)
            trial[agent] = s
            trials.append((self.utility(agent, trial), s))
        best = max(u for u, _ in trials)
        return best, [s for u, s in trials if u == best]

    def strategyproof(self):
        """Exact dominant-strategy truthfulness, with first profitable deviation."""
        choices = [subsets(s) for s in self.ownership]
        for i, own in enumerate(self.ownership):
            others = [j for j in range(len(choices)) if j != i]
            for combination in product(*(choices[j] for j in others)):
                reports = list(self.ownership)
                for j, s in zip(others, combination):
                    reports[j] = s
                truthful = self.utility(i, reports)
                best, responses = self.best_responses(i, reports)
                if best > truthful:
                    return False, {'agent': i, 'others_profile': reports,
                                   'truthful_utility': truthful, 'best_utility': best,
                                   'best_reports': responses}
        return True, None

    def odd_path_condition(self):
        """No same-owner odd directed walk, including positive self-return.

        Parity-expanded BFS terminates with cycles. This conservative condition
        includes walks with repeated vertices; see REPORT.md for the path convention.
        """
        adj = {a: [] for a in self.framework.arguments}
        for a, b in sorted(self.framework.attacks):
            adj[a].append(b)
        for own in self.ownership:
            for source in sorted(own):
                start = (source, 0)
                parents = {start: None}
                queue = deque([start])
                while queue:
                    current, parity = queue.popleft()
                    for target in adj[current]:
                        state = (target, 1 - parity)
                        if state in parents:
                            continue
                        parents[state] = (current, parity)
                        if state[1] == 1 and target in own:
                            route, step = [], state
                            while step is not None:
                                route.append(step[0])
                                step = parents[step]
                            return False, list(reversed(route))
                        queue.append(state)
        return True, None


def jsonable(value):
    if isinstance(value, (set, frozenset)):
        return sorted(value)
    if isinstance(value, (tuple, list)):
        return [jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    return value
