"""
MiniReactor
Minimal reactive programming base.
"""

from collections import namedtuple, defaultdict, deque


class MiniReactor(object):
  """
  # Reactive context.
  # Each context represents a reactive data store
  # and a dependency graph to facilitate automatic
  # change propagation.
  """
  StoreEntry = namedtuple('StoreEntry', ['value', 'dependents'])

  def __init__(self):
    # mapping from stored value -> StoreEntry(value, dependents)
    self.store = defaultdict(lambda: self.StoreEntry(value=None, dependents=set()))
    # queue of functions waiting to be run
    self.queue = deque()
    self.active_fn = None

  def get(self, key):
    """Get a value from the data store."""
    if self.active_fn != None:
      self.store[key].dependents.add(self.active_fn)

    if key in self.store:
      return self.store[key].value
    else:
      return None

  def set(self, key, val):
    """Store or update a value in the data store."""
    self.store[key] = self.StoreEntry(value=val, dependents=self.store[key].dependents)

    for fn in self.store[key].dependents:
      self.queue.append(fn)

    if self.active_fn == None:
      self.autorun(lambda: None)

    return self

  def autorun(self, fn):
    """
    Run a function immediately
    and run it again when data that it depends on changes.
    This is a decorator.
    Please be sure not to create dependencies cycles.
    """
    self.active_fn = fn
    fn()
    self.active_fn = None

    if len(self.queue) > 0:
      self.autorun(self.queue.popleft())


if __name__ == "__main__":
  """Usage Example"""
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
