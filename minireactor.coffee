# Set implementation that is not efficient
# but does support functions as elements.
# This exists to solve the problem whereby functions hash to strings.
class SlowSet
  constructor: (list) ->
    @elements = []
    if list? then @add e for e in list

  add: (e) ->
    @elements.push e unless e in @elements

  contains: (e) -> e in @elements

  size: -> @elements.length


# Reactive context.
class MiniReactor
  constructor: ->
    # mapping from stored values -> their values and dependents
    @values = {}
    # queue of functions waiting to be run
    @queue = []

  get: (key) ->
    if @active_fn?
      @values[key].dependents.add @active_fn

    if key of @values
      @values[key].val
    else
      undefined

  # key should be a string, anything else will be converted to a string
  # val can be anything
  set: (key, val) ->
    @values[key] =
      val: val
      dependents: @values[key]?.dependents or new SlowSet

    for fn in @values[key].dependents.elements
      @queue.push fn

    if not @active_fn?
      @autorun (->)

    return this

  autorun: (fn) ->
    @active_fn = fn
    fn()
    @active_fn = undefined

    if @queue.length > 0
      @autorun @queue.shift()



ctx = new MiniReactor()

ctx.set 'frobnitz', 2
ctx.set 'dingle-arm', true

ctx.autorun ->
  console.log "frobnitz is set to #{ctx.get 'frobnitz'}"

ctx.autorun ->
  if ctx.get 'dingle-arm'
    console.log "watch out for the dingle-arm"
  else
    console.log "dingle-arm disengaged"

ctx.autorun ->
  ctx.set 'frobnitz', 3
  ctx.set 'dingle-arm', false

ctx.set 'frobnitz', 4

# console.log ctx.values
# console.log ctx.functions
