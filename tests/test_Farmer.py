import unittest
from dataserv.Farmer import Farmer, db


class FarmerTest(unittest.TestCase):

    # not working properly
    SQLALCHEMY_DATABASE_URI = "sqlite://dataserv_test.db"
    TESTING = True

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_valid_address(self):
        addr1 = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        addr2 = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc9999ghjfghj99'
        addr3 = 'not valid address'
        addr4 = 'not valid &address'
        addr5 = '791GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'

        farmer1 = Farmer(addr1)
        farmer2 = Farmer(addr2)
        farmer3 = Farmer(addr3)
        farmer4 = Farmer(addr4)
        farmer5 = Farmer(addr5)

        self.assertTrue(farmer1.is_btc_address())
        self.assertFalse(farmer2.is_btc_address())
        self.assertFalse(farmer3.is_btc_address())
        self.assertFalse(farmer4.is_btc_address())
        self.assertFalse(farmer5.is_btc_address())

    def test_address_error(self):
        addr1 = 'not valid address'
        farmer1 = Farmer(addr1)
        self.assertRaises(ValueError, farmer1.validate)

    def test_repr(self):
        addr = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        farmer = Farmer(addr)
        ans = "<Farmer BTC Address: '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'>"
        self.assertEqual(repr(farmer), ans)

    def test_register(self):
        addr1 = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        addr2 = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc9999ghjfghj99'
        addr3 = 'not valid address'

        farmer1 = Farmer(addr1)
        farmer2 = Farmer(addr2)
        farmer3 = Farmer(addr3)

        self.assertFalse(farmer1.exists())
        farmer1.register()
        self.assertTrue(farmer1.exists())

        # test duplicate
        self.assertRaises(ValueError, farmer1.register)

        # these should not be inserted
        self.assertRaises(ValueError, farmer2.register)
        self.assertRaises(ValueError, farmer3.register)

        # double check they are not in the db
        self.assertFalse(farmer2.exists())
        self.assertFalse(farmer3.exists())
