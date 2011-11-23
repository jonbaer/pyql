import unittest

from quantlib.termstructures.yields.rate_helpers import DepositRateHelper
from quantlib.termstructures.yields.piecewise_yield_curve import \
    term_structure_factory
from quantlib.time.api import Date, TARGET, Period, Months
from quantlib.time.api import ModifiedFollowing, Actual365Fixed, ActualActual
from quantlib.time.api import September, ISDA

class PiecewiseYieldCurveTestCase(unittest.TestCase):

    def test_creation(self):

        # Market information
        calendar = TARGET()

        settlement_date = Date(18, September, 2008)
        # must be a business day
        settlement_date = calendar.adjust(settlement_date);

        quotes = [0.0096, 0.0145, 0.0194]
        tenors =  [3, 6, 12]

        rate_helpers = []

        calendar =  TARGET()
        deposit_day_counter = Actual365Fixed()
        convention = ModifiedFollowing
        end_of_month = True

        for quote, month in zip(quotes, tenors):
            tenor = Period(month, Months)
            fixing_days = 3


            helper = DepositRateHelper(
                quote, tenor, fixing_days, calendar, convention, end_of_month,
                deposit_day_counter
            )

            rate_helpers.append(helper)


        ts_day_counter = ActualActual(ISDA)

        tolerance = 1.0e-15

        ts = term_structure_factory(
            'discount', 'loglinear', settlement_date, rate_helpers,
            ts_day_counter, tolerance
        )

        self.assertIsNotNone(ts)

        self.assertEquals( Date(18, September, 2008), ts.reference_date)

        # this is not a real test ...
        self.assertAlmostEquals(0.9975, ts.discount(Date(21, 12, 2008)), 4)
        self.assertAlmostEquals(0.9944, ts.discount(Date(21, 4, 2009)), 4)
        self.assertAlmostEquals(0.9904, ts.discount(Date(21, 9, 2009)), 4)

if __name__ == '__main__':
    unittest.main()
