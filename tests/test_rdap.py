import unittest

from okitsok.rdap import _event_value, _registrar_name


class RdapParsingTests(unittest.TestCase):
    def test_events(self):
        data = {"events": [{"eventAction": "registration", "eventDate": "2020-01-01T00:00:00Z"}]}
        self.assertEqual(_event_value(data, "registration"), "2020-01-01T00:00:00Z")

    def test_registrar_name(self):
        data = {
            "entities": [{
                "roles": ["registrar"],
                "vcardArray": ["vcard", [["fn", {}, "text", "Example Registrar"]]],
            }]
        }
        self.assertEqual(_registrar_name(data), "Example Registrar")


if __name__ == "__main__":
    unittest.main()
