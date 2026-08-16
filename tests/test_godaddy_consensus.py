import unittest

from okitsok.core import resolve_consensus
from okitsok.pricing import _money, _one_year_prices


class ConsensusTests(unittest.TestCase):
    def test_available_when_rdap_and_godaddy_agree(self):
        status, confidence, notes = resolve_consensus("available", "available", True)
        self.assertEqual(status, "available")
        self.assertEqual(confidence, "high")
        self.assertEqual(notes, [])

    def test_registered_when_rdap_and_godaddy_agree(self):
        status, confidence, _ = resolve_consensus("taken", "registered", False)
        self.assertEqual(status, "registered")
        self.assertEqual(confidence, "high")

    def test_conflict_when_rdap_and_godaddy_disagree(self):
        status, confidence, notes = resolve_consensus("unknown", "registered", True)
        self.assertEqual(status, "conflict")
        self.assertEqual(confidence, "none")
        self.assertTrue(notes)

    def test_conflict_when_dns_has_records_but_godaddy_says_available(self):
        status, confidence, _ = resolve_consensus("taken", "unknown", True)
        self.assertEqual(status, "conflict")
        self.assertEqual(confidence, "none")

    def test_dns_only_availability_stays_possible(self):
        status, confidence, _ = resolve_consensus("available", "unknown", None)
        self.assertEqual(status, "possibly_available")
        self.assertEqual(confidence, "low")


class GoDaddyPriceParsingTests(unittest.TestCase):
    def test_money_uses_minor_currency_units(self):
        self.assertEqual(
            _money({"currencyCode": "EUR", "value": 1299}),
            {"value": 12.99, "currency": "EUR"},
        )

    def test_one_year_registration_and_renewal_prices(self):
        registration, renewal = _one_year_prices(
            [
                {
                    "term": "YEAR",
                    "period": 1,
                    "price": {"currencyCode": "EUR", "value": 999},
                    "renewalPrice": {"currencyCode": "EUR", "value": 1999},
                }
            ]
        )
        self.assertEqual(registration["value"], 9.99)
        self.assertEqual(renewal["value"], 19.99)


if __name__ == "__main__":
    unittest.main()
