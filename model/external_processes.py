import datetime
from data.api.yfinance import get_market_prices
from model import constants as constants

def create_market_price_process(date_start, dt, timesteps):
    """Returns a function of (run, timestamp) to be used as price model parameter

    This function will not extrapolate prices to dates where market data is unavailable.

    Therefore your model parameters ("date_start") and simulation configuration ("timesteps" and "dt")
    must result in a simulated time range where market pricing data exists (beginning of ETH/USD market until present time).

    Note that the market data *is cached* on disk for 24hrs.

    See example in notebooks/Feature - Live Price data.

    Args:
        date_start : datetime
            Start date from which to retrieve prices.

        dt : int
            Delta Time used in simulation configuration.
            The unit is "epochs".

        timesteps : int
            Total timesteps of simulation. Together with dt, this is used to determine the end date
            for pricing data retrieval.

    Returns:
        function of (run, timestamp) usable as model parameter.
    """
    market_prices = get_market_prices(
        date_start,
        date_start + datetime.timedelta(days=(timesteps*dt/constants.epochs_per_day)), "1d")

    def price_process(run, timestep):
        # Simulation timesteps do not start from 0, they start from "1 * dt", so we need an off-by-one fix
        day = int(timestep/constants.epochs_per_day) - 1
        return market_prices[day]

    return price_process

