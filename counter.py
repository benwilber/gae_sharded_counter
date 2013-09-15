from random import randint

from google.appengine.ext import db


class ShardedCounter(db.Model):

	SHARD_COUNT = 20

	count = db.IntegerProperty(default=0)


	@classmethod
	def get_random_key_name(cls, base_name):
		index = randint(0, cls.SHARD_COUNT - 1)
		return "%(base_name)s:%(index)d" % locals()


	@classmethod
	def get_all_key_names(cls, base_name):
		return ["%(base_name)s:%(i)d" % locals() for i in xrange(cls.SHARD_COUNT)]


	@classmethod
	def get_all_keys(cls, base_name):
		key_names = cls.get_all_key_names(base_name)
		keys = [db.Key.from_path(cls.kind(), key_name) for key_name in key_names]


	@classmethod
	def get_all_shards(cls, base_name):
		keys = cls.get_all_keys(base_name)
		return filter(None, db.get(keys))


	@classmethod
	def get_shard(cls, base_name):
		key_name = cls.get_random_key_name(base_name)
		shard = cls.get_by_key_name(key_name) or cls(key_name=key_name)
		return shard


	@classmethod
	def get_total(cls, base_name):
		shards = cls.get_all_shards(base_name)
		return sum(shard.count for shard in shards)


	@classmethod
	def incr(cls, base_name, amount=1):
		shard = cls.get_shard(base_name)
		shard.count += amount
		shard.put()


	@classmethod
	def decr(cls, base_name, amount=1):
		cls.incr(base_name, -amount)


	@classmethod
	def reset(cls, base_name):
		keys = cls.get_all_keys(base_name)
		db.delete(keys)



