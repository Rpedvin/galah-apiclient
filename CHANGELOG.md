# Changelog

## Version 1.0-beta.3 (Sept 30, 2013)

A couple of bug fixes (non-critical).

 * An exception that occured before exiting after creating temporary folders was fixed.
 * Improved logging in a few places.

## Version 1.0-beta.2 (Sept 27, 2013)

A number of very useful bug fixes.

 * Fixed a blocking bug in the last release that mandated that the user creates
   a certain directory.
 * Better error reporting all around.
 * Pertinent trace backs can now be enabled with the `--show-tracebacks`
   option.
 * SSL errors are now correctly reported as such (previously reported as
   general connection errors).

## Version 1.0-beta.1 (July 4, 2013)

This is the first major release since the rewrite of the API Client. Tons of
things have changed so make sure to upgrade!

 * Better logging with configurable verbosity.
 * Built-in shell that does not rely on bash, but does have lots of bash
   features like autocomplete and history (even reverse history search).
 * Configuration files are now in YAML.
 * Configuration files can be modified by using the client directly with the `--save` option.
 * Super easy install, just download the binary and go.
 * Download UI is now nicer with progress bars.
 * No more deleting files randomly to get the client to behave.

Let us know what you think!
