from collections import namedtuple, defaultdict, deque


class MiniReactor(object):
  """Reactive Context"""
  StoreEntry = namedtuple('StoreEntry', ['value', 'dependents'])

  def __init__(self):
    # mapping from stored value -> StoreEntry(value, dependents)
    self.store = defaultdict(lambda: self.StoreEntry(value=None, dependents=set()))
    # queue of functions waiting to be run
    self.queue = deque()
    self.active_fn = None

  def get(self, key):
    if self.active_fn != None:
      self.store[key].dependents.add(self.active_fn)

    if key in self.store:
      return self.store[key].value
    else:
      return None

  def set(self, key, val):
    self.store[key] = self.StoreEntry(value=val, dependents=self.store[key].dependents)

    for fn in self.store[key].dependents:
      self.queue.append(fn)

    if self.active_fn == None:
      self.autorun(lambda: None)

    return self

  def autorun(self, fn):
    """Decorator"""
    self.active_fn = fn
    fn()
    self.active_fn = None

    if len(self.queue) > 0:
      self.autorun(self.queue.popleft())


if __name__ == "__main__":
  ctx = MiniReactor()

  ctx.set('frobnitz', 2)
  ctx.set('dingle-arm', True)

  @ctx.autorun
  def render_frobnitz():
    print "frobnitz is set to {}".format(ctx.get('frobnitz'))

  @ctx.autorun
  def render_dinglearm():
    if ctx.get('dingle-arm'):
      print "watch out for the dingle-arm"
    else:
      print "dingle-arm disengaged"

  @ctx.autorun
  def set_things():
    ctx.set('frobnitz', 3)
    ctx.set('dingle-arm', False)

  ctx.set('frobnitz', 4)
