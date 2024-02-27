class Student:

  def __init__(self, students):
    self.students = students
    self.is_student_curriculumn_scheduled = {}
    self.is_student_scheduled = {}

  def student_constraints(self, student, course, day, time):
    if student[
        '_id'] in self.is_student_curriculumn_scheduled:  # student with history of been scheduled
      if self.check_student_schedule(student, day,
                                     time) and self.check_course_schedule(
                                         student, course):  #checking
        self.is_student_curriculumn_scheduled[student['_id']] = [course]
        self.is_student_scheduled[student['_id']] = [day]
        for start, end in time:
          self.is_student_curriculumn_scheduled[student['_id']][day].append(
              (start, end))
        return True
    else:
      # if the student is no history of scheduled
      self.is_student_curriculumn_scheduled[student['_id']] = [course]
      self.is_student_scheduled[student['_id']] = [day]
      for start, end in time:
        self.is_student_curriculumn_scheduled[student['_id']][day].append(
            (start, end))
      return True

  def check_student_schedule(self, student, day, time):
    check = True
    if day in self.is_student_scheduled[
        student['_id']]:  #if student been schedule in the same day
      for start, end in time:
        if (start, end) in self.is_student_scheduled[student['_id']][
            day]:  #check if the student is scheduled in the same time
          check = False  #if the student is scheduled in the same time, return False
          break
    return check  #return True

  def check_course_schedule(self, student, course):
    if course in self.is_student_curriculumn_scheduled[
        student['_id']]:  #if student course has been scheduled
      return False
    else:
      return True
