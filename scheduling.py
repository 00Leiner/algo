import domain
import assignment
import constraints

class Scheduling:

  def __init__(self, _students, _courses, _teachers, _rooms):
    #variable
    self.students = _students
    self.teachers = _teachers
    self.courses = _courses
    self.rooms = _rooms
    self.day = ["Monday", "Tuesday", "Wednesday"]
    self.time = [(7, 8), (8, 9),(9,10),(10,11),(12,13)]

    #dictionry
    self.lab_room = {} # laboratoryroom availability (room, type, time)
    self.lec_room = {} # lectureroom availability (room, type, time)
    self.teacher_availability = {} #teacher availability (teacher, day, time)
    self.assignments = {}

    #populate
    self.domain()
    self.assignment()
    self.constraints()

  def domain(self):
    # Instantiate domain
    domain_instance = domain.domain(self.rooms, self.day, self.time, self.courses, self.teachers)
    self.lab_room = domain_instance.lab_room_domain()
    self.lec_room = domain_instance.lec_room_domain()
    self.teacher_availability = domain_instance.course_teacher_domain()

    
  def assignment(self):
     # Instantiate assignment
    assignment_instance = assignment.assignment(self.students, self.courses, self.teachers, self.rooms, self.day, self.time, self.lab_room, self.lec_room, self.teacher_availability)
    self.assignments = assignment_instance.assignments
    
  def constraints(self):
    # Instantiate constraints
    constraint_instance = constraints.constraints(self.lab_room, self.lec_room)
    self.set_of_time_available = constraint_instance.setOfHoursAvailableInLabRoom(3, self.lec_room)