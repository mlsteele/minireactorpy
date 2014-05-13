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
  """Usage Example"""
  import time

  # create a new reactive context
  ctx = SugarReactor()

  # store initial values for 'location' and 'start_date'
  ctx.location = 'texas'
  ctx.start_date = 1399993421

  # teach it how to render 'location'
  # this will happen once right now
  # this will also happen whenever the value of 'location' is changed
  @ctx
  def render_location():
    location_str = ctx.location.title()
    print "location is set to {}".format(location_str)

  # teach it about the dependency of 'end_date' on 'start_date'
  @ctx
  def sync_dates():
    one_week = 604800 # in seconds
    ctx.end_date = ctx.start_date + one_week

  # teach it how to render 'start_date' and 'end_date'
  @ctx
  def render_dates():
    start_date_str = time.ctime(ctx.start_date)
    end_date_str = time.ctime(ctx.end_date)
    print "departure: {}".format(start_date_str)
    print "return   : {}".format(end_date_str)

  # set some new values for 'location' and 'start_date'
  @ctx
  def set_things():
    ctx.location = 'maine'
    ctx.start_date = 1400993421

  # set a new value for 'location'
  # set's do not have to be run inside 'autorun' blocks
  ctx.location = 'california'
