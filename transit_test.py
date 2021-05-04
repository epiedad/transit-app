import unittest
import transit as EntryClass


class Testing(unittest.TestCase):
    def test_valid_inputs(self):
        a_dict = {
            "card_number": "1",
            "station_in": "A",
            "swipe_in": "2021/05/05 20:00:00"
        }
        entry = EntryClass.Entry(a_dict)
        self.assertTrue(entry.validate_entry())

    def test_invalid_card_number(self):
        a_dict = {
            "card_number": "abc",
            "station_in": "A",
            "swipe_in": "2021/05/05 20:00:00"
        }
        entry = EntryClass.Entry(a_dict)
        self.assertFalse(entry.validate_entry())

    def test_invalid_station_name(self):
        a_dict = {
            "card_number": "1",
            "station_in": "123",
            "swipe_in": "2021/05/05 20:00:00"
        }
        entry = EntryClass.Entry(a_dict)
        self.assertFalse(entry.validate_entry())

    def test_invalid_datetime(self):
        a_dict = {}
        test_time = "2021/05/05 20:00000"
        entry = EntryClass.Entry(a_dict)
        self.assertFalse(entry.is_validatetime(test_time))

    def test_valid_datetime(self):
        a_dict = {}
        test_time = "2021/05/05 20:00:00"
        entry = EntryClass.Entry(a_dict)
        self.assertTrue(entry.is_validatetime(test_time))

if __name__ == '__main__':
    # begin the unittest.main()
    # Run python3 -m unittest transit_test.Testing
    unittest.main()
