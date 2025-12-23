# CAPYFIND

"No AIs, only Capys"
"Don't Worry, Be Capy"

## INSTRUCTIONS

I want a web-based search aggregator.
Searches should be able to be performed on the following search engines:
- Google
- ArviX

In the future we may want to add more, but for now that's good enough. 

## UI

It should be minimal, and it should use the least amount of client-side code possible. We're thinking late 90s style, HackerNews style, where signal is king and noise is filtered out.

Users should be able to toggle the engines to use, and launch a search. We can either merge the results of multiple engines, or we can show them separately, it's up to you. Pagination as needed, but endless scrolling may be too much, it's ok to click next. (unles...?)

We do regular search, not image search or any other type of search.


## Stack

Use Python.
Remember, minimal UI. We don't need no fancy reactive components. Nope. No.

App should be stateless.

## Configuration

Configuration should be done through environment variables. 

GOOGLE_CSE_API_KEY
GOOGLE_CSE_ENGINE_ID

Arvix does not need a key
