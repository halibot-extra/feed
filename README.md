Halibot RSS Reader
==================

Reads and parses RSS and Atom feeds. Will display any new entries in the feed after the last time it checked and starting from when the module first spun up (so it will not display any backlog).

Config Options
--------------

 * `feeds` is an array of urls to grab feeds from. (default [])
 * `delay` is the delay between checking the feeds in seconds. (default 900)
 * `format` is the format string for how to output new entries. See below for more information.
 * `context` the context to which to send the feeds. (Required with a non-empty `feeds` array)


Format Option
-------------

The formatter is given two named arguments, `feed` and `entry`. The formar points to the `feed` element of the result from feedparser, while `entry` refers to the particular entity being output which is equivalent to `entities[j]` for some `j` of the result from feedparser.

See the relevant feedparse documentation [here](https://pythonhosted.org/feedparser/reference.html).

The default format string is as follows:

    {feed.title}: {entry.title}

