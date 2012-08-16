# golocalize
**iOS community driven translations for the iPhone/iPad application FriendCash**


## Locales supported

_Crossed out languages are not yet fully implemented_

- English (en)
- French (fr)
- ~~Spanish (es)~~
- German (de) (Lukas Bestle, [lu-x.me](http://lu-x.me/))


## Contribute

New languages get a copy of the English files so that words not yet translated are easy to identify. Soon 
I'll add a tool to compute the progress of each translation.

### You are a developer ?

Make pull requests and I'll integrate it with pleasure.

#### convert UTF-16 to UTF-8

To convert a single file use 

```sh
$ convert_utf16_to_utf8.sh path/to/file.extension
```

To convert all your git history to UTF-8
> NB: use it only if you know what you are doing

```sh
git filter-branch --tree-filter /absolute/path/to/script/convert_utf16_to_utf8.sh HEAD
```

### You are NOT a developer !

[Download](https://github.com/peteralaoui/golocalize/zipball/master) a copy of the project files, make your changes and email me your modified files at the email address available on [my github profile](https://github.com/peteralaoui).

## Thanks

I want to thanks all the people that contribute to thoses translations, developers or not.

Special thanks to Amy.
