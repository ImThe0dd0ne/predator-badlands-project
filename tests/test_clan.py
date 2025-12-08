import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mechanics.clan import Clan, ClanRank, HonorLogger
from agents.predator import Predator
from utils.location import Location

class ClanTests(unittest.TestCase):

    def test_clan_creation(self):
        clan = Clan("Dark Blade Clan")
        self.assertEqual(clan.get_clan_name(), "Dark Blade Clan")
        self.assertEqual(len(clan.get_hunters()), 0)

    def test_adding_hunters(self):
        clan = Clan("Test Clan")
        dek = Predator("Dek", Location(0, 0))
        
        clan.add_hunter(dek)
        
        self.assertEqual(len(clan.get_hunters()), 1)
        self.assertIn(dek, clan.get_hunters())

    def test_removing_hunters(self):
        clan = Clan("Test Clan")
        dek = Predator("Dek", Location(0, 0))
        
        clan.add_hunter(dek)
        clan.remove_hunter(dek)
        
        self.assertEqual(len(clan.get_hunters()), 0)

    def test_honor_to_rank(self):
        clan = Clan("Test Clan")
        
        self.assertEqual(clan.get_rank(0), ClanRank.UNBLOODED)
        self.assertEqual(clan.get_rank(50), ClanRank.BLOODED)
        self.assertEqual(clan.get_rank(150), ClanRank.HONORED)
        self.assertEqual(clan.get_rank(300), ClanRank.ELITE)
        self.assertEqual(clan.get_rank(500), ClanRank.ELDER)

    def test_judging_actions(self):
        clan = Clan("Test Clan")
        
        good = clan.judge_action("hunt_worthy", {})
        self.assertGreater(good, 0)
        
        bad = clan.judge_action("hunt_weak", {})
        self.assertLess(bad, 0)

    def test_hunter_challenges(self):
        clan = Clan("Test Clan")
        dek = Predator("Dek", Location(0, 0))
        father = Predator("Father", Location(1, 1))
        
        clan.add_hunter(dek)
        clan.add_hunter(father)
        
        result = clan.challenge(dek, father)
        self.assertTrue(result)


class HonorLogTests(unittest.TestCase):

    def test_logger_creation(self):
        dek = Predator("Dek", Location(0, 0))
        logger = HonorLogger(dek)
        self.assertIsNotNone(logger)

    def test_logging_events(self):
        dek = Predator("Dek", Location(0, 0))
        logger = HonorLogger(dek)
        
        logger.log_event("hunt", 20, "Hunted worthy prey")
        
        history = logger.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["type"], "hunt")

    def test_filtering_big_events(self):
        dek = Predator("Dek", Location(0, 0))
        logger = HonorLogger(dek)
        
        logger.log_event("small", 5, "Minor thing")
        logger.log_event("big", 50, "Major achievement")
        logger.log_event("bad", -30, "Bad move")
        
        big_ones = logger.get_big_events()
        self.assertEqual(len(big_ones), 2)


if __name__ == '__main__':
    unittest.main()