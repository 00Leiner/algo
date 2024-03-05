class constraints:
  def __init__(self, lab_room, lec_room):
    self.lab_room = lab_room
    self.lec_room = lec_room
    
  #i need the set of 3 hours consecutive available time for laboratory and list of set of 2 hours consecutive available time for lecture
  def setOfHoursAvailableInLabRoom(self, hrs, labOrLec):
    numberOfHours = hrs
    
    valid_room_day = []
    for room, day in labOrLec.items():
      for day, time in day.items():
        if len(time) >= numberOfHours:
          valid_room_day.append((room, day))

    if len(valid_room_day) == 0:
      print(f"Not enough available slots")
      return False

    available_slots = []
    for r, d in valid_room_day:
      x = [slot for slot, slot_data in labOrLec[r][d].items() if not slot_data]
      available_slots.append(x)

    set_of_available_slot = []
    for set in available_slots:
      print(set)
      for slot in set[:numberOfHours]:
        set_of_available_slot.append(slot)
    print(set_of_available_slot)