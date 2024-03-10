class CSPAlgorithm:
  def __init__(self, students, courses, teachers, rooms):
      # Initialization code
    self.students = students
    self.courses = courses
    self.teachers = teachers
    self.rooms = rooms
    self.schedule = {}  # {course_id: {'teacher': teacher_id, 'room': room_id, 'schedule': (day, time)}}
    self.initialize_domains()
    self.backtracking_search()
    #print(self.schedule)
    
  def initialize_domains(self):
    # Initialize the domains for each course with all possible combinations of teachers, rooms, and times
    for student in self. students:
      student_id = student['_id']
      self.schedule[student_id] = {}
      for course in student['courses']:
        course_code = course['code']
        
        self.schedule[student_id][course_code] = {'teacher': None, 'room': None, 'schedule': None}
        
        teachers_for_course = [teacher['_id'] for teacher in self.teachers if course_code in [t['code'] for t in teacher['specialized']]]
        
        rooms_for_course = [room['_id'] for room in self.rooms if room['types'] == course['types']]
  
        self.schedule[student_id][course_code]['teacher'] = teachers_for_course
        self.schedule[student_id][course_code]['room'] = rooms_for_course
        self.schedule[student_id][course_code]['schedule'] = None

  def backtracking_search(self):
    return self.backtrack({})

  def backtrack(self, assignment):
    if len(assignment) == len(self.schedule):
        return assignment  # Return the complete assignment

    course_id = self.select_unassigned_course(assignment)
    for teacher_id in self.schedule[student_id][course_id]['teacher']:
        for room_id in self.schedule[student_id][course_id]['room']:
            for time_slot in self.schedule[student_id][course_id]['schedule']:
                if self.is_assignment_valid(course_id, teacher_id, room_id, time_slot):
                    assignment[course_id] = {'teacher': teacher_id, 'room': room_id, 'schedule': time_slot}
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                    assignment.pop(course_id)  # Backtrack if no valid assignment found
    return None  # No valid assignment found

  def select_unassigned_course(self, assignment):
    x ={}
    for student_id in self.schedule:
      x[student_id] = []
      for course_id in self.schedule[student_id]:
          if course_id not in assignment:
            x[student_id].append(course_id)
          else: 
            break
    return x
