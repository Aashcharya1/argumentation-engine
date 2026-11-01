import itertools
import unittest
from engine import ArgumentationFramework as AF, GroundedMechanism, subsets
from server import analyse


class EngineTests(unittest.TestCase):
    def test_textbook_examples(self):
        from book_examples import example_5_10, example_5_11
        game = example_5_10()
        self.assertEqual(game.outcome(game.ownership), {'a1','a3'})
        self.assertEqual([game.utility(i, game.ownership) for i in range(3)], [1,0,1])
        reports = [{'a4','a5'}, {'a2'}, {'a3'}]
        self.assertEqual(game.outcome(reports), {'a2','a4','a5'})
        self.assertEqual(game.utility(0, reports), 2)
        self.assertFalse(game.strategyproof()[0])
        game = example_5_11()
        self.assertEqual(game.outcome(game.ownership), {'a1','a4','a5','a6'})
        self.assertTrue(game.strategyproof()[0])
        self.assertFalse(game.odd_path_condition()[0])

    def test_chain(self):
        af = AF('abc', [('a', 'b'), ('b', 'c')])
        self.assertEqual(af.grounded_extension(), {'a', 'c'})
        self.assertTrue(af.defends({'a'}, 'c'))
        self.assertFalse(af.conflict_free({'a', 'b'}))
        self.assertEqual(af.characteristic(set()), {'a'})

    def test_mutual(self):
        af = AF('ab', [('a', 'b'), ('b', 'a')])
        self.assertEqual(set(af.complete_extensions()), {frozenset(), frozenset('a'), frozenset('b')})
        self.assertEqual(len(af.legal_labellings()), 3)
        self.assertEqual(af.acceptance_status('a', 'preferred'), 'credulously accepted')

    def test_odd_cycle_and_self_attack(self):
        for af in [AF('abc', [('a','b'), ('b','c'), ('c','a')]), AF('a', [('a','a')])]:
            self.assertEqual(af.stable_extensions(), [])
            self.assertEqual(af.grounded_extension(), set())
            self.assertIn('undefined', af.acceptance_status('a', 'stable'))

    def test_hiding_and_ties(self):
        af = AF('abc', [('a','b'), ('b','c')])
        game = GroundedMechanism(af, [{'a','b'}, {'c'}])
        self.assertTrue(game.strategyproof()[0])
        # Profitable hiding: a -> b -> c -> d, own a,d; hide a to accept d.
        af = AF('abcd', [('a','b'), ('b','c'), ('c','d'), ('d','a')])
        game = GroundedMechanism(af, [{'a','d'}, {'b','c'}])
        self.assertFalse(game.strategyproof()[0])
        self.assertFalse(game.odd_path_condition()[0])

    def test_validation_empty_and_api(self):
        self.assertEqual(AF([], []).complete_extensions(), [frozenset()])
        with self.assertRaises(ValueError):
            AF('a', [('a','b')])
        with self.assertRaises(ValueError):
            GroundedMechanism(AF('ab', []), [{'a'}, {'a','b'}])
        self.assertEqual(analyse(dict(arguments=['a'], attacks=[]))['extensions']['grounded'], [['a']])

    def test_all_three_node_graphs_against_independent_labellings(self):
        args = 'abc'
        edges = list(itertools.product(args, repeat=2))
        for mask in range(1 << len(edges)):
            af = AF(args, [e for j, e in enumerate(edges) if mask & (1 << j)])
            legal = []
            for values in itertools.product(['in', 'out', 'undec'], repeat=3):
                lab = dict(zip(args, values))
                valid = True
                for a in args:
                    attackers = [lab[b] for b in af.attackers[a]]
                    expected = 'out' if 'in' in attackers else 'in' if all(x == 'out' for x in attackers) else 'undec'
                    valid &= lab[a] == expected
                if valid:
                    legal.append(lab)
            self.assertEqual({tuple(sorted(x.items())) for x in legal},
                             {tuple(sorted(x.items())) for x in af.legal_labellings()})
            grounded = af.grounded_extension()
            self.assertTrue(all(grounded <= s for s in af.complete_extensions()))
            self.assertTrue(all(s in af.preferred_extensions() for s in af.stable_extensions()))

    def test_parity_cycles(self):
        game = GroundedMechanism(AF('abc', [('a','b'),('b','c'),('c','a')]), [{'a'},{'b'},{'c'}])
        ok, path = game.odd_path_condition()
        self.assertFalse(ok)
        self.assertEqual((len(path)-1) % 2, 1)


if __name__ == '__main__':
    unittest.main()
