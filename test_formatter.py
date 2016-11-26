from unittest import TestCase
from run import SerialRunner
from formatter import Formatter


class TestFormatter(TestCase):
    def test_run_hama(self):
        runner = SerialRunner("HamadryasSim", 50, 2)
        output = runner.run()

        formatter = Formatter(output)
        for_out = formatter.format()

        self.assertTrue(for_out)
        self.assertEqual(len(output), len(for_out))

    def test_run_sav(self):
        runner = SerialRunner("SavannahSim", 50, 2)
        output = runner.run()

        formatter = Formatter(output)
        for_out = formatter.format()

        self.assertTrue(for_out)
        self.assertEqual(len(output), len(for_out))
