import unittest

from okitsok.market import extract_asking_price


class MarketTests(unittest.TestCase):
    def test_extract_usd_buy_now_price(self):
        self.assertEqual(extract_asking_price("Buy now for $2,499"), (2499.0, "USD"))

    def test_extract_eur_price(self):
        self.assertEqual(extract_asking_price("Asking price: € 12 500"), (12500.0, "EUR"))

    def test_no_price(self):
        self.assertIsNone(extract_asking_price("Make an offer for this domain"))


if __name__ == "__main__":
    unittest.main()
