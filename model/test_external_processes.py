import pytest
import datetime

from model.external_processes import create_market_price_process

def test_market_price_process():
    date_start = datetime.datetime(2021, 1, 1)
    dt = 225 # that's 225 epochs in a day
    timesteps = 5 # our simulation range will be 5 days (with the above `dt`)

    pr = create_market_price_process(date_start, dt=dt, timesteps=timesteps)

    for (timestep, expected_price) in [
        (1, 737.71), # First day and price
        (2, 730.4),  # 2nd day
        (5, 1041.5), # 5th day
    ]:
        assert pr(0, timestep * dt) == expected_price

    # Raises 'out of bounds' when simulation exceeds timesteps
    with pytest.raises(Exception) as ex:
        pr(0, dt*(timesteps + 1))

    assert ex.match(r"out of bounds")

