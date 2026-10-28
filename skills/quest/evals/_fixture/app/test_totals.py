import unittest

from totals import invoice_total


class InvoiceTotalTest(unittest.TestCase):
    def test_sums_lines(self):
        self.assertEqual(invoice_total([(2.5, 2), (1.0, 3)]), 8.0)

    def test_empty_invoice(self):
        self.assertEqual(invoice_total([]), 0)


if __name__ == "__main__":
    unittest.main()
