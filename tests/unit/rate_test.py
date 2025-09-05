import time
from app.rate.limiter import TokenBucket, cost_for_input_tokens

def test_cost_rounds_up():
    assert cost_for_input_tokens(1) == 1
    assert cost_for_input_tokens(250) == 1
    assert cost_for_input_tokens(251) == 2

def test_token_bucket_basic():
    tb = TokenBucket(capacity=3, refill_rate=1.0)
    uid = "u"
    ok, retry = tb.consume(uid, 1)
    assert ok and retry == 0
    ok, retry = tb.consume(uid, 2)
    assert ok
    ok, retry = tb.consume(uid, 1)
    assert not ok and retry > 0
    time.sleep(1.1)
    ok, retry = tb.consume(uid, 1)
    assert ok
