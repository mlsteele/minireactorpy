class MiniReactor
  constructor: ->
    # mapping from stored values -> their values and dependents
    @values = {}
    @queue = []

  get: (key) ->
    console.log "get(#{key})"

    if @active_fn?
      @values[key].dependents.push @active_fn

    if key of @values
      @values[key].val
    else
      undefined

  set: (key, val) ->
    console.log "set(#{key}, #{val})"

    @values[key] =
      val: val
      dependents: @values[key]?.dependents or []

    for dep in @values[key].dependents
      @queue.push dep

    return this

  autorun: (fn) ->
    @active_fn = fn
    fn()
    @active_fn = undefined

    if @queue.length > 0
      @autorun @queue.shift()


ctx = new MiniReactor()

ctx.autorun ->
  ctx.set 'foo', 2

ctx.autorun ->
  console.log "foo is now #{ctx.get 'foo'}"

ctx.autorun ->
  ctx.set 'foo', 3

ctx.autorun ->
  ctx.set 'foo', 4

console.log ctx.values
console.log ctx.functions
