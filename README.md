# marquote

Django rewrite of the [marquote-cli](https://github.com/rixx/marquote-cli) project.

Provides a website for marquote chain generation.
Provides an admin interface to add, edit and delete different kinds of project, data and chain generators.

The main markov logic resides in the markov app (data model of words and sentences, abstract and example parser and
project), Projects themselves each get their own app, and, if required, parser.

(This approach was chosen because projects requirements can vary a lot; a Shakespeare sonnet generator does different
things from a Bible generator or a Star Trek generator).
