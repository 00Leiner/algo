from domain.student_curriculum_domain import student_curriculum_domain
from domain.availability_domain import teacher_availability_domain
from domain.availability_domain import student_availability_domain
from domain.availability_domain import room_availability_domain
from domain.assignment_domain import assignmnet_domain
from constraints.unassigned_course import select_unassigned_course
from constraints.schedule import update_schedule
from constraints.schedule import undo_update_schedule
from constraints.validate_assignmnet import validate_assignmnet

class CSPAlgorithm:

  def __init__(self, students, courses, teachers, rooms):
    # Initialization code
    self.students = students
    self.courses = courses
    self.teachers = teachers
    self.rooms = rooms
    self.timeslots = range(7,19)
    self.days = range(1, 7)
    #domain
    self.domain_schedule = {}  # {course_id: {'teacher': teacher_id, 'room': room_id, 'schedule': (day, time)}}
    self.student_curriculum = [] # (teacher_id, course_id)
    self.teachers_schedule = {}  # {teacher_id: {day: {timeslot: []}}}
    self.students_schedule = {}  # {student: {day: {timeslot: []}}}
    self.rooms_schedule = {}  # {room: {day: {timeslot: []}}}
    self.course_unit = {}  #dictionarry to define course unit
    self.course_type = {}  #dictionarry to define course type
    self.initialize_domains()
    self.backtracking_search()
    print(self.backtracking_search())

  def initialize_domains(self):
    self.student_curriculum = student_curriculum_domain(self.students)
    self.teachers_schedule = teacher_availability_domain(self.teachers, self.days, self.timeslots)
    self.students_schedule = student_availability_domain(self.students, self.days, self.timeslots)
    self.rooms_schedule = room_availability_domain(self.rooms, self.days, self.timeslots)
    self.course_unit = {course['code']: course['units'] for course in self.courses}
    self.course_type = {course['code']: course['types'] for course in self.courses}

    _assignmnet_domain = assignmnet_domain(self.student_curriculum, self.teachers,self.course_type, self.rooms, self.days, self.timeslots)
    self.domain_schedule = _assignmnet_domain.assignment_domain()

  def backtracking_search(self, num_solutions=5):
    solutions = []
    self.backtrack({}, solutions, num_solutions)
    return solutions

  def backtrack(self, assignment, solutions, num_solutions):
    validate = validate_assignmnet(self.teachers_schedule, self.rooms_schedule, self.students_schedule, self.days)

    if len(solutions) == num_solutions:
        # Stop the search if the desired number of solutions is reached
        return

    list_domain_schedule = self.domain_schedule
    if len(assignment) == len(list_domain_schedule):
        # Solution found, append it to the list of solutions
        solutions.append(assignment.copy())  # Use copy to avoid modifying the original assignment
        return

    unassign_student = select_unassigned_course(assignment, list_domain_schedule)
    if unassign_student:
      student_id, course_code = unassign_student
      for teacher_id in self.domain_schedule[(student_id, course_code)]['teacher']:
        for first_schedule in self.domain_schedule[(student_id, course_code)]['schedule']['first']:
          for first_day_room_id in self.domain_schedule[(student_id, course_code)]['schedule']['first_day_room']:
            for second_schedule in self.domain_schedule[(student_id, course_code)][ 'schedule']['second']:
              for second_day_room_id in self.domain_schedule[(student_id, course_code)]['schedule']['second_day_room']:
                if validate.is_assignmnet_valid(assignment, student_id, course_code, teacher_id, first_schedule, first_day_room_id, second_schedule, second_day_room_id):
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

                    teacher_sched = self.teachers_schedule
                    student_sched = self.students_schedule
                    room_sched = self.rooms_schedule
                    update_schedule(student_id,teacher_id, first_day_room_id, first_schedule, teacher_sched, student_sched, room_sched)
                    update_schedule(student_id,teacher_id, second_day_room_id, second_schedule, teacher_sched, student_sched, room_sched)
                    
                    # Recursively backtrack
                    self.backtrack(assignment, solutions, num_solutions)
                      
                    # Backtrack if no solution found
                    assignment.pop((student_id, course_code))  # Remove after assigning
                    #undo
                    undo_update_schedule(student_id,teacher_id, first_day_room_id, first_schedule, teacher_sched, student_sched, room_sched)
                    undo_update_schedule(student_id,teacher_id, second_day_room_id, second_schedule, teacher_sched, student_sched, room_sched)
    
    return None
