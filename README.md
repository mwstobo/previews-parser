# Previews Parser
A parser for PreviewsWorld text files containing new comic book release info.

Note that the parser will only return comics published by the following
companies:
- Marvel Comics
- DC Comics
- Image Comics
- Dark Horse Comics
- IDW Publishing

This is because PreviewsWorld does not specify publishers for any other
releases.  It simply categorizes them under "Comics & Graphic Novels".

Also note that the parser will only return comic book releases.  It will
ignore trade paperbacks and hardcovers as well as anything categorized as a
toy.

## Example usage
```
import previews_parser

f = open('newreleases.txt', 'r')
string = f.read()
output = previews_parser.parse(string)

# process output...
```

## Tests
If you want to run the test suite, simply install `nosetests` and then run
`nose`.
