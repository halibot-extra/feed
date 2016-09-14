import time
import asyncio
import feedparser
from threading import Thread
from halibot import HalModule, Message, Context

DEFAULT_DELAY = 900

class FeedModule(HalModule):

	def init(self):
		self.alive = True
		self.last_entries = {}
		self.last_time = time.gmtime()
		cxt = Context(**self.config['context'])

		self.loop = asyncio.SelectorEventLoop()
		self.thread = Thread(target=self.loop.run_forever)
		self.thread.start()
		self.schedule_next()

	def shutdown(self):
		self.loop.call_soon_threadsafe(self.loop.stop)
		self.thread.join()

	# Schedule the next time the feeds will be parsed
	def schedule_next(self):
		delay = self.config.get('delay', DEFAULT_DELAY)
		self.loop.call_soon_threadsafe(self.loop.call_later, delay, self.parse_feeds)

	# Retrieve a feed, handles etags and last modified stuff
	def retrieve_feed(self, url):
		l = self.last_entries.get(url, {})
		etag = l.get('etag', None)
		modified = l.get('modified', None)

		self.log.info('Requesting feed: ' + str(url))

		f = feedparser.parse(url, etag=etag, modified=modified)
		if f.feed != {}:
			self.last_entries[url] = f
		else:
			self.log.info('No additional information retrieved')

		return f

	# Called when there is a new entry found
	def handle_new_entry(self, feed, entry):
		d = dict(feed=feed, entry=entry)
		fmt = self.config.get('format', '{feed.title}: {entry.title}')
		body = fmt.format(**d)
		cxt = Context(**self.config['context'])

		self.log.info('New entry: "{}"'.format(body))

		# TODO make more sensible
		self.reply(Message(body=body, context=cxt))

	# Parse all of the give feeds
	def parse_feeds(self):
		urls = self.config.get('feeds', [])
		newtime = time.gmtime()

		for url in urls:
			f = self.retrieve_feed(url)
			for ent in f.entries:
				# Check that the entry is new (if we can)
				if not 'modified_parsed' in ent or self.last_time < ent.modified_parsed:
					self.handle_new_entry(f.feed, ent)

		self.last_time = newtime
		self.schedule_next()

