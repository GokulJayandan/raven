import unittest
from raven.core import world,episode,greedy_match,exact_match,clarification
class TestRaven(unittest.TestCase):
    def test_generation(self):
        p=world(42,n=24);self.assertEqual(len(p),24);self.assertEqual(len({x.id for x in p}),24)
    def test_matching_nonoverlap(self):
        weights={(0,1):.8,(0,2):.7,(1,3):.9,(2,3):.3}
        for solve in (greedy_match,lambda w:exact_match([0,1,2,3],w)):
            val,pairs=solve(weights);self.assertEqual(len({k for pair in pairs for k in pair}),2*len(pairs))
    def test_exact_beats_greedy(self):
        w={(0,1):.9,(0,2):.7,(1,3):.7,(2,3):.05}
        self.assertGreater(exact_match(list(range(4)),w)[0],greedy_match(w)[0])
    def test_policy_budget(self):
        people=world(12,n=24);active=[x.id for x in people if x.status!='declined']
        for policy in ('none','fifo','endpoints','singleton','portfolio','persistent'):
            selected=clarification(people,active,set(),policy,world(41,n=100),1)
            self.assertLessEqual(len(selected),4)
            self.assertTrue(all(people[i].status=='recoverable' for i in selected))
    def test_reproducible(self):
        self.assertEqual(episode(73,'portfolio'),episode(73,'portfolio'))
if __name__=='__main__':unittest.main()
