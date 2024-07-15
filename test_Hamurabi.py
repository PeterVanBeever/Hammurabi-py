import unittest
import sys
import os

# Ensure the correct path for importing Hammurabi
sys.path.insert(0, '/Users/peter/Dev/Hammurabi-py')

from HamurabiV8 import Hammurabi  # Adjust the import based on your actual file name

class HammurabiTest(unittest.TestCase):
    def setUp(self):
        self.ham = Hammurabi()

    def about(self, expected, actual):
        return 0.90 * expected < actual < 1.10 * expected

    def testPlagueDeaths1(self):
        number_of_plagues = 0
        for i in range(10000):
            deaths = self.ham.plagueDeaths(100)
            if deaths > 0:
                number_of_plagues += 1
        percentPlagues = number_of_plagues / 100
        self.assertTrue(self.about(1500, number_of_plagues), f"Number of plagues is about {percentPlagues}, not about 15%.")

    def testPlagueDeaths2(self):
        deaths = 0
        for i in range(10000):
            deaths = self.ham.plagueDeaths(100)
            if deaths > 0:
                break
        self.assertEqual(deaths, 50, f"In a plague, {deaths}% of your people die, not 50%.")

    def testStarvationDeaths(self):
        deaths = self.ham.starvationDeaths(100, 1639)
        self.assertEqual(deaths, 19, "Wrong number of starvation deaths.")
        deaths = self.ham.starvationDeaths(100, 2500)
        self.assertGreaterEqual(deaths, 0, "You starved a negative number of people!")

    def testUprising(self):
        self.assertTrue(self.ham.uprising(1000, 451), "Should have had an uprising!")
        self.assertFalse(self.ham.uprising(1000, 449), "Should not have had an uprising!")

    def testImmigrants(self):
        imm = self.ham.immigrants(10, 1200, 500)
        self.assertEqual(imm, 25, "Wrong number of immigrants.")

    def testHarvest(self):
        yield_ = [0] * 7
        for i in range(1000):
            harvest = self.ham.harvest(1)
            self.assertTrue(0 < harvest <= 6, f"Illegal harvest per acre: {harvest}")
            yield_[harvest] += 1
        for j in range(1, 7):
            self.assertGreater(yield_[j], 0, f"You never have a yield of {j} bushels per acre.")

    def testGrainEatenByRats1(self):
        infestations = 0
        for i in range(1000):
            eaten = self.ham.grainEatenByRats(100)
            if eaten > 0:
                infestations += 1
        percentInfestations = infestations / 100
        self.assertTrue(self.about(400, infestations), f"Number of rat infestations is about {percentInfestations}, not about 40%.")

    def testGrainEatenByRats2(self):
        counts = [0] * 31
        for i in range(10000):
            percent = self.ham.grainEatenByRats(100)
            if percent == 0:
                continue
            counts[percent] += 1
            self.assertTrue(10 <= percent <= 30, f"Rats ate {percent}% of your grain, not 10% to 30%.")
        for j in range(11, 30):
            self.assertGreater(counts[j], 0, f"Rats never ate {j}% of your grain.")

    def testNewCostOfLand(self):
        cost = [0] * 24
        for i in range(1000):
            price = self.ham.newCostOfLand()
            self.assertTrue(17 <= price <= 23, f"Illegal cost of land: {price}")
            cost[price] += 1
        for j in range(17, 24):
            self.assertGreater(cost[j], 0, f"You never have a land cost of {j} bushels per acre.")

if __name__ == '__main__':
    unittest.main()
