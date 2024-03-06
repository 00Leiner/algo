    '''            
    # Find the day with enough available slots to accommodate all units
    available_slots = self.constraint_instance.search_for_avaialable_slot_in_room(hrsInLab, self.lab_room)

    if len(available_slots) == 0:
      print(f"Not enough available slots to assign for course {course['_id']}")
      return

    for room, day in available_slots:
      for slot in available_slots[(room,day)][:hrsInLab]:
        check_teacher_availability = self.teacher_assignment(course_code, day, slot)
        if check_teacher_availability:
          # Find the day with enough available slots for second schedule with 2 days gap from the previousschedule  
          pass
          '''