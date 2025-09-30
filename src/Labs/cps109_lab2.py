def make_bricks(small, big, goal):

  b = big*5
  d = goal - b


  #if ( (goal - round(goal/5) * 5) * 5 ) + small == goal:
  #  return True

  bbrick_diff = goal - (goal%5) if (goal >= 5) else None

  # Determine if you have required amnt of bircks
  if (b >= bbrick_diff) and (goal - ((bbrick_diff/5) * 5)) <= small:
    return True


  #if True:
  #  return bbrick_diff

  if (d > 0) and (small>=d):
    return True

  if (b==goal) or (small==goal) or (b+small==goal):
    return True

  return False
