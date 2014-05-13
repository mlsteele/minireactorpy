from minireactor import MiniReactor, SugarReactor

def example_minireactor():
  """MiniReactor Usage Example"""
  import time

  # create a new reactive context
  ctx = MiniReactor()

  # store initial values for 'location' and 'start_date'
  ctx.set('location', 'texas')
  ctx.set('start_date', 1399993421)

  # teach it how to render 'location'
  # this will happen once right now
  # this will also happen whenever the value of 'location' is changed
  @ctx.autorun
  def render_location():
    location_str = ctx.get('location').title()
    print "location is set to {}".format(location_str)

  # teach it about the dependency of 'end_date' on 'start_date'
  @ctx.autorun
  def sync_dates():
    one_week = 604800 # in seconds
    ctx.set('end_date', ctx.get('start_date') + one_week)

  # teach it how to render 'start_date' and 'end_date'
  @ctx.autorun
  def render_dates():
    start_date_str = time.ctime(ctx.get('start_date'))
    end_date_str = time.ctime(ctx.get('end_date'))
    print "departure: {}".format(start_date_str)
    print "return   : {}".format(end_date_str)

  # set some new values for 'location' and 'start_date'
  @ctx.autorun
  def set_things():
    ctx.set('location', 'maine')
    ctx.set('start_date', 1400993421)

  # set a new value for 'location'
  # set's do not have to be run inside 'autorun' blocks
  ctx.set('location', 'california')


def example_sugarreactor():
  """SugarReactor Usage Example"""
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


if __name__ == "__main__":
  example_sugarreactor()
