import datetime
import time


class RateLimiterTokenBucket:

    last_refill_timestamp: datetime.datetime

    def __init__(self, capacity: int, win_time_seconds: int):
        self.capacity = capacity
        self.win_time_seconds = win_time_seconds
        self.last_refill_timestamp = datetime.datetime.now()
        self.refill_count_per_sec = capacity / win_time_seconds
        self.available_tokens = 0  # Starts at zero

    def get_available_tokens(self):
        return self.available_tokens

    def refill(self):
        now = datetime.datetime.now()

        if now > self.last_refill_timestamp:
            elapsed_time = now - self.last_refill_timestamp
            # print(f'elapsed_time={elapsed_time.microseconds / 1000}\ncurrent:  {now}\nprevious: {self.last_refill_timestamp}')
            tokens_to_add = (elapsed_time.microseconds / 1000000) * self.refill_count_per_sec
            if tokens_to_add > 0:
                print(f'{now}: Adding {tokens_to_add} tokens (refill_count_per_sec={self.refill_count_per_sec})')
                self.available_tokens = min(self.capacity, self.available_tokens + tokens_to_add)
                self.last_refill_timestamp = now

    def try_consume(self):

        self.refill()

        if self.available_tokens > 0:
            self.available_tokens -= 1
            print(f'Succeeded, available_tokens={self.available_tokens}')
        else:
            print(f'Rate Limited')
            return False


def main():
    rate_limiter = RateLimiterTokenBucket(6, 3)
    count = 1000
    while count > 0:
        time.sleep(0.2)
        rate_limiter.try_consume()
        count -= 1


if __name__ == '__main__':
    main()