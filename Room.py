class Room:
  def __init__(self, room, day, time):
    self.room = room
    self.room_capacity = {} #make sure no overlapping schedule [room_id, day, time]

  def room_constraints(self, room, day, time):
    if room['_id'] in self.room_capacity:
      if day in self.room_capacity[room['_id']]:
        if self.check_timeslot_available(room, day, time):
          for start, end in time:
            self.room_capacity[room['_id']][day].append((start, end))
          return True
      else:
        self.room_capacity[room['_id']][day] = []
        for start, end in time:
          self.room_capacity[room['_id']][day].append((start, end))
        return True
    else:
      self.room_capacity[room['_id']] = {}
      self.room_capacity[room['_id']][day] = []
      for start, end in time:
        self.room_capacity[room['_id']][day].append((start, end))
      return True

  def check_timeslot_available(self, room, day, time):
    check = True
    for start, end in time:
      if (start, end) in self.room_capacity[room['_id']][day]:
        check = False
        break
    return check


  