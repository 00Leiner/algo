class Student:
  def __init__(self, students):
    self.students = students
    self.student_curriculumn_schedule = {}

  def student_constraints(self, student, course, day, time):
    if student['_id'] in self.student_curriculumn_schedule:
      if course in self.student_curriculumn_schedule[student['_id']]:
        return False
      else:
        self.student_curriculumn_schedule[student['_id']].append(course) = {}
        #need to check if the teacher is been scheduled with the same day and time
        
        
    else:
      self.student_curriculumn_schedule.append([student['_id']][course][day][(start, end) for start, end in time]])
      #need to check if the teacher is been scheduled with the same day and time
        