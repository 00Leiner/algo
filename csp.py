from sys import setdlopenflags


class CSPAlgorithm:

  def __init__(self, students, courses, teachers, rooms):
    # Initialization code
    self.students = students
    self.courses = courses
    self.teachers = teachers
    self.rooms = rooms
    self.timeslots = range(7,19)
    self.days = range(1, 7)
    self.schedule = {}  # {course_id: {'teacher': teacher_id, 'room': room_id, 'schedule': (day, time)}}
    self.student_curriculum = [] # (teacher_id, course_id)
    self.teachers_schedule = {}  # {teacher_id: {day: {timeslot: []}}}
    self.students_schedule = {}  # {student: {day: {timeslot: []}}}
    self.rooms_schedule = {}  # {room: {day: {timeslot: []}}}
    self.course_unit = {}  #dictionarry to define course unit
    self.course_type = {}  #dictionarry to define course type
    self.initialize_domains()
    self.backtracking_search()
    #print(self.schedule)

  def initialize_domains(self):
    self.student_curriculum_domain()
    self.schedule_availability_domain()
    self.course_domain()
    self.assignment_domain()

  def student_curriculum_domain(self):
    for student in self.students:
        student_id = student['_id']
        for course in student['courses']:
            course_code = course['code']
            self.student_curriculum.append((student_id, course_code))
    
  def schedule_availability_domain(self):
    self.teachers_schedule = {
        teacher['_id']: {
            day: {
                time: []
                for time in self.timeslots
            }
            for day in self.days
        }
        for teacher in self.teachers
    }
    self.students_schedule = {
        student['_id']: {
            day: {
                time: []
                for time in self.timeslots
            }
            for day in self.days
        }
        for student in self.students
    }
    self.rooms_schedule = {
        room['_id']: {
            day: {
                time: []
                for time in self.timeslots
            }
            for day in self.days
        }
        for room in self.rooms
    }

  def course_domain(self):
    self.course_unit = {
        course['code']: course['units']
        for course in self.courses
    }
    self.course_type = {
        course['code']: course['types']
        for course in self.courses
    }

  def assignment_domain(self):
    for student_id, course_code in self.student_curriculum:

        self.schedule[(student_id,course_code)] = {
            'teacher': None,
            'schedule': {
                'first': None,
                'first_day_room': None,
                'second': None,
                'second_day_room': None
            }
        }

        teachers_for_course = [
            teacher['_id'] for teacher in self.teachers
            if course_code in [t['code'] for t in teacher['specialized']]
        ]
      
        course_type = self.course_type[course_code]
        rooms_for_first_day = self.room_assignment(course_type)

        rooms_for_second_day = self.room_assignment('lecture')

        first_sched = self.first_day_schedule(course_code)

        second_sched = {}
        for _day, _ in first_sched:
          second_sched = self.second_day_schedule(course_code, _day)

        self.schedule[(student_id,course_code)]['teacher'] = teachers_for_course
        self.schedule[(student_id,course_code)]['schedule']['first'] = first_sched
        self.schedule[(student_id,course_code)]['schedule']['first_day_room'] = rooms_for_first_day
        self.schedule[(student_id,course_code)]['schedule']['second'] = second_sched
        self.schedule[(student_id,course_code)]['schedule']['second_day_room'] = rooms_for_second_day

  def room_assignment(self, course_type):
    set_of_room = []
    for room in self.rooms:
      if room['types'] == course_type:
        set_of_room.append(room['_id'])
        return room['_id']

  def first_day_schedule(self, course_code):
    type = self.course_type[course_code]
    list_of_timeslots = list(self.timeslots)
    time_schedule = []
    if type == 'laboratory':
      #3 hours in laboratory
      for day in self.days:
        for i in range(len(list_of_timeslots) - 3):
          set_of_3 = (day, (list_of_timeslots[i], list_of_timeslots[i + 3]))
          time_schedule.append(set_of_3)
    
    if type == 'lecture':
      #3 hours in lecture
      for day in self.days:
        for i in range(len(list_of_timeslots) - 2):
          set_of_2 = (day, (list_of_timeslots[i], list_of_timeslots[i + 2]))
          time_schedule.append(set_of_2)
          
    return time_schedule

  def second_day_schedule(self, course_code, first_day):
    type = self.course_type[course_code]
    list_of_timeslots = list(self.timeslots)
    list_of_days = list(self.days)

    #2 days gap from first schedule
    first_day_index = list_of_days.index(first_day)
    second_day_index = (first_day_index + 4) % len(list_of_days)
    second_day = list_of_days[second_day_index]

    if type == 'laboratory':
      # 2 hours in lecture
      sets_of_time_in_lecture = []
      for i in range(len(list_of_timeslots) - 2):
        _timeslot = (second_day, (list_of_timeslots[i], list_of_timeslots[i + 2]))
        sets_of_time_in_lecture.append(_timeslot)
      return sets_of_time_in_lecture

    if type == 'lecture':
      # 2 hours in lecture
      sets_of_time_in_lecture = []
      for i in range(len(list_of_timeslots) - 1):
        _timeslot = (second_day, (list_of_timeslots[i], list_of_timeslots[i + 1]))
        sets_of_time_in_lecture.append(_timeslot)

      return sets_of_time_in_lecture

  def backtracking_search(self):
    return self.backtrack({})

  def backtrack(self, assignment):
    if len(assignment) == len(self.schedule):
      return assignment  # Return the complete assignment

    unassign_student = self.select_unassigned_course(assignment)
    if unassign_student:
      student_id, course_code = unassign_student
      for teacher_id in self.schedule[(student_id, course_code)]['teacher']:
          for first_schedule in self.schedule[(student_id, course_code)][
              'schedule']['first']:
            for first_day_room_id in self.schedule[(student_id, course_code)][
                'schedule']['first_day_room']:
              for second_schedule in self.schedule[(student_id, course_code)][
                  'schedule']['second']:
                for second_day_room_id in self.schedule[(student_id, course_code)]['schedule']['second_day_room']:
                  if self.is_assignmnet_valid(assignment, student_id, course_code, teacher_id, first_schedule, first_day_room_id, second_schedule, second_day_room_id):
                    # Assign course to student
                    assignment[(student_id, course_code)] = {
                        'teacher': teacher_id,
                        'schedule': {
                            'first': first_schedule,
                            'first_day_room': first_day_room_id,
                            'second': second_schedule,
                            'second_day_room': second_day_room_id
                        }
                    }
                    
                    self.update_schedule(student_id,teacher_id, first_day_room_id, first_schedule)
                    self.update_schedule(student_id,teacher_id, second_day_room_id, second_schedule)
                    
                    # Recursively backtrack
                    result = self.backtrack(assignment)
                    if result is not None:
                      #print(result)
                      return result
                      
                    # Backtrack if no solution found
                    assignment.pop((student_id, course_code))  # Remove after assigning
                    #undo
                    self.undo_update_schedule(student_id,teacher_id, first_day_room_id, first_schedule)
                    self.undo_update_schedule(student_id,teacher_id, second_day_room_id, second_schedule)
    
    return None
  
  def select_unassigned_course(self, assignment):
    unassigned_courses = {}
    for (student_id, course_code) in self.schedule:
      if (student_id, course_code) not in assignment:
        return (student_id, course_code)
    return unassigned_courses

  def update_schedule(self, student_id, teacher_id, room_id, sched):
    _day, _time = sched
    
    for t in range(_time[0], (_time[1] + 1)): # the plus 1 is for rest before continues schedule
      self.teachers_schedule[teacher_id][_day][t].append('occupied')
      self.students_schedule[student_id][_day][t].append('occupied')
      
    for t in range(_time[0], (_time[1])):
      self.rooms_schedule[room_id][_day][t].append('occupied')

  def undo_update_schedule(self, student_id, teacher_id, room_id, sched):
    _day, _time = sched

    # Undo changes made to teachers_schedule and students_schedule
    for t in range(_time[0], (_time[1] + 1)):
        self.teachers_schedule[teacher_id][_day][t].remove('occupied')
        self.students_schedule[student_id][_day][t].remove('occupied')

    # Undo changes made to rooms_schedule
    for t in range(_time[0], (_time[1])):
        self.rooms_schedule[room_id][_day][t].remove('occupied')

  def is_assignmnet_valid(self, assignment, student_id, course_code, teacher_id, first_schedule, room_id_for_first_schedule, second_schedule, room_id_for_second_schedule):
    print(assignment)
    if not self.is_teacher_available(teacher_id, first_schedule): #check teacher availability in first schedule
      return False
    if not self.is_teacher_available(teacher_id, second_schedule): #check teacher availability in second schedule
      return False
    if not self.is_room_available(room_id_for_first_schedule, first_schedule):  #check room availability in first schedule
      return False
    if not self.is_room_available(room_id_for_second_schedule, second_schedule): #check room availability in second schedule
      return False
    if not self.is_student_available(student_id, first_schedule): #check teacher availability in first schedule
      return False
    if not self.is_student_available(student_id, second_schedule): #check teacher availability in second schedule
      return False
    
    return True

  def is_teacher_available(self, teacher_id, sched):
    #ensure 1 day rest
    if not self._ensure_etacher_restday(teacher_id, sched):
      return False
    #check if time is available
    if not self._check_teacher_time_availability(teacher_id, sched):
      return False
    return True

  def _ensure_etacher_restday(self, teacher_id, sched):
    ensure_rest_day = []

    #get all day that has schedule
    for day in self.teachers_schedule[teacher_id]:
      for time in self.teachers_schedule[teacher_id][day]:
        if self.teachers_schedule[teacher_id][day][time]:
          ensure_rest_day.append(day)
          break
    #check if the schedule still have rest
    _day, _time = sched
    if _day not in ensure_rest_day:
      if len(ensure_rest_day) == (len(self.days) - 1):
        return False
      else:
        return True
    else:
      return True

  def _check_teacher_time_availability(self, teacher_id, sched):
    if sched:
      _day, _time = sched 
      for t in range(_time[0], (_time[1]) + 1): # the plus 1 check if the time next to it is represent as rest
        if self.teachers_schedule[teacher_id][_day][t]:
          return False
        else:
          return True
    else:
      return False
      
  def is_room_available(self, room_id, sched):
    if sched:
      _day, _time = sched 
      for t in range(_time[0], (_time[1])):
        if self.rooms_schedule[room_id][_day][t]:
          return False
        else:
          return True
    else:
      return False

  def is_student_available(self, student_id, sched):
    if sched:
      _day, _time = sched 
      for t in range(_time[0], (_time[1])):
        if self.students_schedule[student_id][_day][t]:
          return False
        else:
          return True
    else:
      return False
