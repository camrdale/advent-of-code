## Visualizer for Intcode Operations

This directory contains a webapp for visualizing the operations that were run by
an Intcode program.

To use the web app, first run the Web Dev Server to serve the webapp:

```
npm run build && npm run serve
```

For development, run `npm run build:watch` and `npm run serve` in separate
terminals, so you can edit and see changes as they are made.

To generate and load the data from an Intcode program run, pass `visualize=True`
to the `intcode.Program` constructor, then run the program. It will output a
`FOO.json` file to the `year2019/visualizer/dumps` directory, where `FOO` is the
name of the program passed to the constructor. Then load the JSON file in the
URL of the dev server: http://localhost:8000/dev/index.html?f=FOO.json
