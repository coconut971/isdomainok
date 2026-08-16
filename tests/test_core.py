import unittest

from okitsok.core import expand_domains, normalize_tlds


class CoreTests(unittest.TestCase):
    def test_normalize_tlds(self):
        self.assertEqual(normalize_tlds(["com", ".AI", "com"]), [".com", ".ai"])

    def test_expand_base_names_and_exact_domains(self):
        self.assertEqual(
            expand_domains(["LightSRaw", "example.net"], ["com", "fr"]),
            ["lightsraw.com", "lightsraw.fr", "example.net"],
        )


if __name__ == "__main__":
    unittest.main()
