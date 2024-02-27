class Room:
  def __init__(self, room, day, time):
    self.room = room
    self.room_capacity = {} #make sure no overlapping schedule [room_id, day, time]

  def room_constraints(self, student, type, day, time):
    pass


  