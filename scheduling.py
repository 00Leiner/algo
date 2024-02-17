import Teachers


class Scheduling:

  def __init__(self, _students, _courses, _teachers, _rooms):
    #variable
    self.students = _students
    self.teachers = _teachers
    self.courses = _courses
    self.rooms = _rooms
    self.day = ["Monday", "Tuesday"]
    self.time = [(7, 8), (8, 9)]

    #domain
    self.student_domain = {}
    self.teacher_domain = {}
    self.course_code_domain = {}
    self.course_types_domain = {}
    self.room_domain = {}


    #populate
    self.domain()
    self.teacher()

  def domain(self):
    for student in self.students:
      self.student_domain[student['_id']] = [
          course['code'] for course in student['courses']
      ]

    for teacher in self.teachers:
      self.teacher_domain[teacher['_id']] = [
          course['code'] for course in teacher['specialized']
      ]

    for course in self.courses:
      self.course_code_domain[course['_id']] = [(course['code'])]
      self.course_types_domain[course['_id']] = [(course['types'])]

    for room in self.rooms:
      self.room_domain[room['_id']] = [(room['types'])]

  def teacher(self):
    teachers = self.teacher_domain
    max_daily_hours = 6
    max_continuous_hours = 3
    max_day_in_week = 5
    #print(teachers)
    Teachers.Teacher(teachers, max_daily_hours, max_continuous_hours,
                     max_day_in_week)
