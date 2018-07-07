# slackstub
Slack stub for local development integration testing.

Persists resources during a single run, so you can query for what you've added.
`/meta` API calls exist to allow meta calls (API calls to affect API calls,
  e.g. to accept pending invites).

[![asciicast](https://asciinema.org/a/sz25qnLTcPzrigx9OPGHfrIMV.png)](https://asciinema.org/a/sz25qnLTcPzrigx9OPGHfrIMV)

## Usage

The goal is to maintain parity with https://api.slack.com/web (and others?) For now:
- All calls must be POSTs
- All arguments must be sent as POST parameters, presented as `application/x-www-form-urlencoded` (this needs to change -- slack has some cases where JSON is fine but others where it's not, part of the value of this stub should be to highlight those edge cases before you get to hitting slack for real.)
- It doesn't matter if you provide an `Authorization` header: not auth is implemented

See API Calls for a list of implemented calls and their status.

Example: `curl -F 'email=jonny@bravo' -X POST localhost:5000/api/users.admin.invite`

### Docker (recommended)

`docker run -p 5000:5000 andytumelty/slackstub:latest`

### Standalone

Requirements:
- python3
- flask

`./server.py`

The flask server will bind to `localhost:5000`.


## API calls


|endpoint|parameters|development status|
|---|---|---|
|`/api/auth.test`| _None_ | Done -- always succeeds. Warning: A random user_id is generated and returned for each call.|
|`/api/users.list`| <ul><li>next_cursor (optional)</li><li>limit (optional)</li></ul> | Core functionality done -- no error handling for bad cursors or limits, and maximum limits don't match slack|
|`/api/users.admin.invite`| *email | Done, plus slack errors for `already_in_team` and `already_invited` |
|`/api/users.admin.setInactive`| *email | Core functionality done -- this is a paid only feature, that error isn't done yet though. No error handling. |
|`/meta/invite.accept`| *email | Accepts invite for the given email. No error handling. |
|`/meta/invite.accept.all`| _None_ | Accepts all invites. No error handling. |


## Development

PR's welcome -- super WIP right now, and probably minimal development until I
need the API calls/hit the use cases.

API endpoint requests also welcome, even better with example request/response
detail. Raise an issue and I'll estimate the work.

## TODO

- (Optional SSL)
- The major slack APIs
- Tests
