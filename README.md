# MiniReactor
Minimal reactive programming base for python.

```bash
python minireactor.py
```

## Example Usage

```python
# create a new reactive context
ctx = MiniReactor()

# store initial values for 'frobnitz' and 'dingle-arm'
ctx.set('frobnitz', 2)
ctx.set('dingle-arm', True)

# teach it how to render 'frobnitz'
# this will happen once right now
# this will also happen whenever the value of 'frobnitz' is changed
@ctx.autorun
def render_frobnitz():
  print "frobnitz is set to {}".format(ctx.get('frobnitz'))

# teach it how to render 'dingle-arm'
@ctx.autorun
def render_dinglearm():
  if ctx.get('dingle-arm'):
    print "watch out for the dingle-arm"
  else:
    print "dingle-arm disengaged"

# set some new values for 'frobnitz' and 'dingle-arm'
@ctx.autorun
def set_things():
  ctx.set('frobnitz', 3)
  ctx.set('dingle-arm', False)

# set a new value for 'frobnitz'
# set's do not have to be run inside 'autorun' blocks
ctx.set('frobnitz', 4)
```

```
frobnitz is set to 2
watch out for the dingle-arm
frobnitz is set to 3
dingle-arm disengaged
frobnitz is set to 4
```
