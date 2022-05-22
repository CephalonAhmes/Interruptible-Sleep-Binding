import InterruptibleSleepBinding
import time

def test_sleep_without_signal():
    initial_time = time.time()
    response = InterruptibleSleepBinding.sleep_for_x_milliseconds(55)
    post_time = time.time()
    assert(post_time - initial_time > 0.05)
    