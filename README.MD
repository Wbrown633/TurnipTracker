This is a simple discord bot written using the python API to track the turnip
prices of multiple users in a server.

The following functionality is supported in `v0.3`

- The default syntax is `$turnip (price) [AM/PM] [MM/DD/YY]`
  - `(price)` is required and is the price to be recorded
  - `[AM/PM]` is an optional argument to set the period
  - `[MM/DD/YY]` is an optional argument to set the date
Additionally multiple flags are supported

- `--user [username]` sets the username
- `--debug` sets the storage sheet to the debug sheet for testing
- `--master` sets the storage sheet to sheet1
- `--status` checks the status of the TurnipBot
