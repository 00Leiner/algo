class constraints:
  def __init__(self, lab_room, lec_room):
    self.lab_room = lab_room
    self.lec_room = lec_room
    
  def search_for_avaialable_slot_in_room(self, day, hrs, list_of_room):
    # Find the day with enough available slots to accommodate all units
    available_day = None
    for day, slots in day.items():
      available_slots = sum(1 for slot in slots.values() if not slot)
      if available_slots >= hrs:
        available_day = day
        break
          
    # Assign units to available slots on the chosen day
    available_slots = {}
    available_slots[available_day] = []
    for slot, slot_data in list_of_room[available_day].items():
      if not slot_data:
        available_slots[available_day].append(slot)

    return available_slots

  def search_for_avaialable_slot_for_second_schedule(self, hrs, list_of_room, day):
    pass