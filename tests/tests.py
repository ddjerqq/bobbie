import unittest
from models.user import User


class UserTest(unittest.TestCase):
    def test_something(self):
        amount = 15
        this  = User.new(1, "this")
        this.wallet = 10
        this.bank   = 20
        # test if we can withdraw and send money

        recv = 0

        if this.wallet >= amount:
            this.wallet -= amount
            recv += amount
        elif this.wallet + this.bank >= amount:
            amount -= this.wallet
            this.wallet = 0
            this.bank -= amount
            recv = amount

        self.assertEqual(this.bank, 15)
        self.assertEqual(recv, amount)




if __name__ == "__main__":
    unittest.main()
