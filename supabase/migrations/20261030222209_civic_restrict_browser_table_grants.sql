/*
# Restrict browser access to civic issue tables

1. Modified Tables
- `issues`: browsers keep only SELECT and INSERT. UPDATE and DELETE are removed.
- `officer_credentials` and `officer_sessions`: all browser access is removed.

2. Security
- Default database privileges had granted every action to the public roles on new tables. Those extra grants are revoked here.
- Row level security policies on `issues` are unchanged.

3. Important Notes
1. Status changes are made only by the officer function, which runs with server rights after checking the officer token.
*/

REVOKE ALL ON issues FROM anon, authenticated;
GRANT SELECT, INSERT ON issues TO anon, authenticated;

REVOKE ALL ON officer_credentials FROM anon, authenticated;
REVOKE ALL ON officer_sessions FROM anon, authenticated;
