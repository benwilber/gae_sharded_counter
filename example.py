
from .counter import ShardedCounter


def main():

	ShardedCounter.incr("signups", 1)
	ShardedCounter.incr("api_requests", 10)
	ShardedCounter.decr("api_requests", 1)
	ShardedCounter.get_total("api_requests")
	ShardedCounter.reset("api_requests")


if __name__ == '__main__':

	main()


