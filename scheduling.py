class Scheduling:

  def __init__(self, _students, _courses, _teachers, _rooms):
    #variable
    self.students = _students
    self.teachers = _teachers
    self.courses = _courses
    self.rooms = _rooms
    self.day = ["Monday", "Tuesday", "Wednesday"]
    self.time = [(7, 8), (8, 9),(9,10),(10,11),(12,13)]

    #dictionry for domain
    self.lab_room = {} # laboratory room availability 
    self.lec_room = {} # lecture room availability 
    self.teacher_availability = {} # teacher availability
    self.student_availability = {} # student availability
    
    self.list_of_available_teacher_in_course = {} #teachers who can teach a course
    
    #schedule
    self.schedule = {}

    #populate
    self.domain()
    self.student_assignment()
    

  def domain(self):
    self.lab_room = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.rooms if room['types'] == 'laboratory'}
    
    self.lec_room = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.rooms if room['types'] == 'lecture'}

    self.teacher_availability = {teacher['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for teacher in self.teachers}

    self.student_availability = {student['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for student in self.students}
    
    self.list_of_available_teacher_in_course = {course['code']: {teacher['_id'] for teacher in self.teachers if course['code'] in [t['code'] for t in teacher['specialized']]} for course in self.courses}

  def student_assignment(self):
    for student in self.students:
      for course in student['courses']:
        self.course_assignment(student['_id'], course['code'])

  def course_assignment(self, student_id, course_code):
    for course in self.courses:
      if course['code'] == course_code:
          type = course['types']

          if type == 'laboratory':
            hrsInLab = 3
            hrsInLec = 2
            laboratory_room = self.lab_room
            self.room_assignment(hrsInLab, laboratory_room)
            
  def room_assignment(self, hrs, list_of_room):
      set_of_slots = {}
  
      # Iterate through each room and its availability
      for room, days in list_of_room.items():
          set_of_slots[room] = {}  # Initialize the inner dictionary for the current room
          for day, time in days.items():
              set_of_slots[room][day] = []  # Initialize the list for the current day
              time_available = [slot for slot, slotData in time.items() if not slotData]  # Remove the timeslot that has been scheduled
  
              n = len(time_available)
              if n >= hrs:
                  sequences = []
                  for i in range(n - 2):  # Stop at the third-to-last index
                      sequence = time_available[i:i+3]
                      set_of_slots[room][day].append(sequence)
  
      return set_of_slots
        

  def teacher_assignment(self, course_code, day, time):
      #check if the teacher is available on the given day and time
      getTeacher = None
      for teacher_id in self.teacher_specialization[course_code]:
        if teacher_id in self.teacher_availability:
          if day in self.teacher_availability[teacher_id]:
            for t in time:
              if t in self.teacher_availability[teacher_id][day]:
                continue
              else: 
                #self.teacher_availability[teacher_id][day].append(time)
                getTeacher = teacher_id
                break
          else:
            #self.teacher_availability[teacher_id][day] = [time]
            getTeacher = teacher_id
            break
        else:
          #self.teacher_availability[teacher_id] = {day: [time]}
          getTeacher = teacher_id
          break

      if getTeacher is None:
        print('No Teacher is available for', course_code)

      return getTeacher

  def student_availability_constraints(self, student_id):
    pass