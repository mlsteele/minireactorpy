"""
MiniReactor
Minimal reactive programming base.

SugarReactor
Prettier reactive programming base.
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


class SugarReactor(object):
  """
  Wraps a MiniReactor so that it can be used
  with more syntactic niceties.
  """
  def __init__(self):
    # hide the reactor away in a name with dashes
    # because dot-accesses can't have dashes
    self.__dict__['data-store'] = MiniReactor()

  def __getattr__(self, key):
    return self.__dict__['data-store'].get(key)

  def __setattr__(self, key, value):
    self.__dict__['data-store'].set(key, value)

  def __call__(self, fn):
    self.__dict__['data-store'].autorun(fn)


if __name__ == "__main__":
  import examples
  examples.example_sugarreactor()
