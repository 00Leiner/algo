import domain
import assignment

class Scheduling:

  def __init__(self, _students, _courses, _teachers, _rooms):
    #variable
    self.students = _students
    self.teachers = _teachers
    self.courses = _courses
    self.rooms = _rooms
    self.day = ["Monday", "Tuesday", "Wednesday"]
    self.time = [(7, 8), (8, 9),(9,10),(10,11),(12,13)]

    #domain
    self.lab_room = {} # laboratoryroom availability (room, type, time)
    self.lec_room = {}# lectureroom availability (room, type, time)
    self.teacher_availability = {} #teacher availability (teacher, day, time)
    self.domain_instance = domain.domain(self.rooms, self.day, self.time, self.courses, self.teachers) # domain implementation

    #assingmnet
    self.assignments = {}
    self.assingment_instance = assignment.assignment(self.students, self.courses, self.teachers, self.rooms, self.day, self.time, self.lab_room, self.lec_room, self.teacher_availability) # assignment implementation
    
    #populate
    self.domain()
    self.assignment()
    
  def domain(self):
    self.lab_room = self.domain_instance.lab_room_domain()
    self.lec_room = self.domain_instance.lec_room_domain()
    self.teacher_availability = self.domain_instance.course_teacher_domain()

    
  def assignment(self):
    self.assignments = self.assingment_instance.assignments
    
  def constraints(self):
    pass