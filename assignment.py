class assignment:
  def __init__(self, _students, _courses, _teachers, _rooms, _day, _time, _lab_room, _lec_room, teacher_availability):
    self.students = _students
    self.teachers = _teachers
    self.courses = _courses
    self.rooms = _rooms

    self.assignments ={}
    print('apple')

  def student_assignment(self):
    for student in self.students:
      for course in student['courses']:
        self.course_assignment(student['_id'], course['code'])

  def course_assignment(self, student_id, course_code):
    for course in self.courses:
      if course['code'] == course_code:
          type = course['types']

          if type == 'laboratory':
              # Number of hours required for laboratory sessions
              num_of_hour_in_lab = 3

              # Find a room and day that lab_room have enough time slots 
              available_lab_room = None 
              for room, day_schedule in self.lab_room.items():
                  for day, time_slots in day_schedule.items():
                      if len(time_slots) >= num_of_hour_in_lab:
                          available_lab_room = (room, day)
                          break

              # If no room and day available, then return False
              if available_lab_room is None:
                  print(f"Not enough available slots in laboratory room to assign all units for student {student_id} course {course['code']}")
                  return

              # Assign units to available slots on the chosen room and day
              available_slots_in_lab_room = [slot for slot, slot_data in self.lab_room[available_lab_room[0]][available_lab_room[1]].items() if not slot_data]

              for slot in available_slots_in_lab_room[:num_of_hour_in_lab]:
                  lab_day = available_lab_room[1]
                  teacher_id = self.get_teacher_available(course_code, day, slot)

                  if teacher_id is not None:

                    # Number of hours required for laboratory sessions
                    num_of_hour_in_lac = 2

                    # Find a room and day that lab_room have enough time slots 
                    available_lec_room = None 
                    for room, day_schedule in self.lab_room.items():
                        for day, time_slots in day_schedule.items():
                            if len(time_slots) >= num_of_hour_in_lac:
                                available_lab_room = (room, day)
                                break

                    # If no room and day available, then return False
                    if available_lec_room is None:
                        print(f"Not enough available slots in lecture room to assign all units for student {student_id} course {course['code']}")
                        return

                    # Assign units to available slots on the chosen room and day
                    available_slots_in_lec_room = [slot for slot, slot_data in self.lec_room[available_lec_room[0]][available_lab_room[1]].items() if not slot_data]


                    '''
                      # Update schedule with the assigned course unit
                      self.lab_room[available_lab_room[0]][lab_day][slot] = (student_id, course_code, teacher_id)
                      print(self.lab_room)
                      print(f"Assigned {course_code} to student {student_id} in room {available_slots_in_lab_room[0]} on {lab_day} at slot {slot} with teacher {teacher_id}")'''
                  else:
                      print(f"No teacher available for course {course_code} at {day}, slot {slot}")

  
    def teacher_assignment(self):
      #check if the teacher is available on the given day and time
      getTeacher = None
      for teacher_id in self.course_teacher_assignments[course_code]:
        if teacher_id in self.teacher_availability:
          if day in self.teacher_availability[teacher_id]:
            if time in self.teacher_availability[teacher_id][day]:
              continue
            else: 
              self.teacher_availability[teacher_id][day].append(time)
              getTeacher = teacher_id
              break
          else:
            self.teacher_availability[teacher_id][day] = [time]
            getTeacher = teacher_id
            break
        else:
          self.teacher_availability[teacher_id] = {day: [time]}
          getTeacher = teacher_id
          break

      if getTeacher is None:
        print('No Teacher is available for', course_code)

      return getTeacher
