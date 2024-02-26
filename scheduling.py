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

    #populate
    self.teacher()
    self.assignment()

    #generatede_schedule
    self.generate_schedule = {}

  def student(self):
    students = self.students
    

  def teacher(self):
    teachers = self.teachers
    max_daily_hours = 6
    max_continuous_hours = 3
    max_day_in_week = 5
    #print(teachers)
    Teachers.Teacher(teachers, max_daily_hours, max_continuous_hours,
                     max_day_in_week)
    

  def assignment(self):
    for student in self.students:
      for curr_course_code in student['courses']:
        for teacher in self.teachers:
          for specialized_code in teacher['specialized']:
            for course in self.courses:
              for room in self.rooms:
                for day in self.day:
                  for time in self.time:
                    if (curr_course_code['code'] == course['code']
                        and specialized_code['code'] == course['code']
                        and course['types'] == room['types']):
                      print(student['_id'], curr_course_code['code'], teacher['_id'],
                            specialized_code['code'], course['code'], room['_id'], day,
                            time)
