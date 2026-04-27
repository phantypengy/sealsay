# Seal creation instructions

All seals added here must be ONLY named
`name.txt` where name is the name of the seal.

DO NOT append extra stuff to the seal names such as doing:
`basicseal.txt` this should be `basic.txt`

This is due to how seals are auto-added to the README.md in root

You use two comments to define the eyes/tongues of seals. they should be comma seperated:

- `# eyes: {.} {.}` (anything inside the {}'s will be what is actually replaced with user provided eyes)
- `# tongues: (__{/\}__)` (anything inside the {}'s will be what is actually replaced with user provided tongues)

e.g with multiple eyes/tongues in one seal file:

```
# eyes: {6} {6}, {a} {a}, {6} {6}
# tongues: (_{x}_ ), (_{x}_), ( _{x}_)
```

notice the comma seperation. Generally, you should include stuff around the areas you want to replace and just brace the actual replace-ee since it'll find the match easier and with less possiblity for accidental/unintended replaces
