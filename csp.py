class CSPAlgorithm:

  def __init__(self, students, courses, teachers, rooms):
    # Initialization code
    self.students = students
    self.courses = courses
    self.teachers = teachers
    self.rooms = rooms
    self.timeslots = [(7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
    self.days = ["Monday", "Tuesday", "Wednesday", 'Thuesday']
    self.schedule = {
    }  # {course_id: {'teacher': teacher_id, 'room': room_id, 'schedule': (day, time)}}
    self.teachers_schedule = {}  # {teacher_id: {day: {timeslot: []}}}
    self.students_scheudle = {}  # {student: {day: {timeslot: []}}}
    self.rooms_schedule = {}  # {room: {day: {timeslot: []}}}
    self.course_unit = {}  #dictionarry to define course unit
    self.course_type = {}  #dictionarry to define course type
    self.initialize_domains()
    self.backtracking_search()
    #print(self.course_type)

  def initialize_domains(self):
    self.schedule_availability_domain()
    self.course_domain()
    self.assignment_domain()

  def schedule_availability_domain(self):
    self.teachers_schedule = {
        teacher['_id']: {
            day: {
                time: []
                for time in range(7, 19)
            }
            for day in range(1, 7)
        }
        for teacher in self.teachers
    }
    self.students_scheudle = {
        student['_id']: {
            day: {
                time: []
                for time in range(7, 19)
            }
            for day in range(1, 7)
        }
        for student in self.students
    }
    self.rooms_schedule = {
        room['_id']: {
            day: {
                time: []
                for time in range(7, 19)
            }
            for day in range(1, 7)
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
    for student in self.students:
      student_id = student['_id']
      self.schedule[student_id] = {}
      for course in student['courses']:
        course_code = course['code']

        self.schedule[student_id][course_code] = {
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

        rooms_for_first_day = [
            room['_id'] for room in self.rooms
            if room['types'] == course['types']
        ]
        rooms_for_second_day = [
            room['_id'] for room in self.rooms
            if room['types'] == 'lecture' or 'Lecture'
        ]

        first_sched = [(_day, _time) for _day, _time in self.first_day_schedule(course_code)]
        
        second_sched = None
        for _day, _ in first_sched:
          second_sched = self.second_day_schedule(course_code, _day)

        self.schedule[student_id][course_code]['teacher'] = teachers_for_course
        self.schedule[student_id][course_code]['schedule'][
            'first'] = first_sched
        self.schedule[student_id][course_code][
            'first_day_room'] = rooms_for_first_day
        self.schedule[student_id][course_code]['schedule'][
            'second'] = second_sched
        self.schedule[student_id][course_code][
            'second_day_room'] = rooms_for_second_day

  def first_day_schedule(self, course_code):
    type = self.course_type[course_code]

    if type == 'laboratory':
      #3 hours in laboratory
      hrs = 3
      sets_of_time_in_laboratory = []

      for day in self.days:
        for i in range(len(self.timeslots) - 2):
          set_of_3 = (day, (self.timeslots[i][0], self.timeslots[i + 2][1]))
          sets_of_time_in_laboratory.append(set_of_3)

      return sets_of_time_in_laboratory

    if type == 'lecture':
      #3 hours in lecture
      hrs = 2
      sets_of_time_in_lecture = []

      for day in self.days:
        for i in range(len(self.timeslots) - 1):
          set_of_2 = (day, (self.timeslots[i][0], self.timeslots[i + 1][1]))
          sets_of_time_in_lecture.append(set_of_2)

      return sets_of_time_in_lecture

  def second_day_schedule(self, course_code, first_day):
    type = self.course_type[course_code]

    #2 days gap from first schedule
    first_day_index = self.days.index(first_day)
    second_day_index = (first_day_index + 2) % len(self.days)
    second_day = self.days[second_day_index]

    if type == 'laboratory':
      # 2 hours in lecture
      sets_of_time_in_lecture = []

      for i in range(len(self.timeslots) - 1):
        _timeslot = (second_day, (self.timeslots[i][0],
                                  self.timeslots[i + 1][1]))
        sets_of_time_in_lecture.append(_timeslot)

      return sets_of_time_in_lecture

    if type == 'lecture':
      # 2 hours in lecture
      sets_of_time_in_lecture = []

      for i in range(len(self.timeslots)):
        _timeslot = (second_day, (self.timeslots[i]))
        sets_of_time_in_lecture.append(_timeslot)

      return sets_of_time_in_lecture

  def backtracking_search(self):
    return self.backtrack({})

  def backtrack(self, assignment):
    if len(assignment) == len(self.schedule):
      return assignment  # Return the complete assignment

    student_curriculum = self.select_unassigned_course(assignment)
    for student_id, curriculum in student_curriculum.items():
      for course_code in curriculum:
        for teacher_id in self.schedule[student_id][course_code]['teacher']:
          for first_schedule in self.schedule[student_id][course_code][
              'schedule']['first']:
            for first_day_room_id in self.schedule[student_id][course_code][
                'first_day_room']:
              for second_schedule in self.schedule[student_id][course_code][
                  'schedule']['second']:
                for second_day_room_id in self.schedule[student_id][
                    course_code]['second_day_room']:
                  if self.is_assignmnet_valid(assignment, student_id,
                                              course_code, teacher_id,
                                              first_schedule,
                                              first_day_room_id,
                                              second_schedule,
                                              second_day_room_id):
                    assignment[student_id][course_code] = {
                        'teacher': teacher_id,
                        'schedule': {
                            'first': first_schedule,
                            'first_day_room': first_day_room_id,
                            'second': second_schedule,
                            'second_day_room': second_day_room_id
                        }
                    }
                    #first schedule
                    for assigned_day, assigned_time in first_schedule.items():
                      for assigned_timeslot in assigned_time:
                        self.teachers_schedule[teacher_id][assigned_day][
                            assigned_timeslot].append('occupied')
                        self.students_scheudle[student_id][assigned_day][
                            assigned_timeslot].append('occupied')
                        self.rooms_schedule[first_day_room_id][assigned_day][
                            assigned_timeslot].append('occupied')
                    #second schedule
                    for second_assigned_day, second_assigned_time in first_schedule.items(
                    ):
                      for assigned_timeslot in second_assigned_time:
                        self.teachers_schedule[teacher_id][
                            second_assigned_day][assigned_timeslot].append(
                                'occupied')
                        self.students_scheudle[student_id][
                            second_assigned_day][assigned_timeslot].append(
                                'occupied')
                        self.rooms_schedule[second_day_room_id][second_assigned_day][
                            assigned_timeslot].append('occupied')

                    result = self.backtrack(assignment)
                    if result is not None:
                      return result
                    assignment[student_id].pop(
                        course_code)  #remove after assigning
    return None

  def select_unassigned_course(self, assignment):
    x = {}
    for student_id in self.schedule:
      x[student_id] = []
      for course_id in self.schedule[student_id]:
        if course_id not in assignment:
          x[student_id].append(course_id)
        else:
          break
    return x

  def is_assignmnet_valid(self, assignment, student_id, course_code, teacher_id, first_schedule, room_id_for_first_schedule, second_schedule, room_id_for_second_schedule):
    pass
