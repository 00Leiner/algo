class Scheduling:

  def __init__(self, _students, _courses, _teachers, _rooms):
    #variable
    self.students = _students
    self.teachers = _teachers
    self.courses = _courses
    self.rooms = _rooms
    self.day = ["Monday", "Tuesday", "Wednesday"]
    self.time = [(7, 8), (8, 9),(9,10),(10,11),(12,13), (13,14)]

    #dictionry for domain
    self.lab_room = {} # laboratory room availability 
    self.lec_room = {} # lecture room availability 
    self.teacher_availability_dic = {} # teacher availability
    self.student_availability_dic = {} # student availability
    
    #schedule
    self.schedule = {}

    #populate
    self.domain()
    self.assignment()
    
  def domain(self):
    self.lab_room = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.rooms if room['types'] == 'laboratory'}
    
    self.lec_room = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.rooms if room['types'] == 'lecture'}

    self.teacher_availability_dic = {teacher['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for teacher in self.teachers}

    self.student_availability_dic = {student['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for student in self.students}
    
    self.list_of_available_teacher_in_course = {course['code']: {teacher['_id'] for teacher in self.teachers if course['code'] in [t['code'] for t in teacher['specialized']]} for course in self.courses}


  def assignment(self):
    for student in self.students:
      student_id = student['_id']
      for course in student['courses']:
        type = course['types']
        course_id = course['code']

        if type == 'laboratory':
          hrsInLab = 3
          hrsInLec = 2
          laboratory_room = self.lab_room
          availability_of_student = self.student_availability(student_id, hrsInLab)
          for day, timeslot in availability_of_student.items():
            for set in timeslot:
              room_available = self.room_availability(laboratory_room, day, set)
              #if room_available:
               # is_teachers_available = self.teacher_availability(course_id, day, set)

  def student_availability(self, student_id, NumOfHrs):
    available_slots = {}
  
    if student_id in self.student_availability_dic:
        for day, time in self.student_availability_dic[student_id].items():
            available_indices = [(time_slot, slotData) for time_slot, slotData in time.items()]
            available_slots[day] = []  # Initialize list for the current day
            for i in range(len(available_indices) - (NumOfHrs - 1)):
                set_indices = available_indices[i:i + NumOfHrs]
                if all(not slotData for _, slotData in set_indices):  # Check if all slots in the set are empty
                    available_slots[day].append([slot for slot, _ in set_indices])
   
    return available_slots
              
          
  def room_availability(self, list_of_room, day, setOfTime):
      # Iterate through each room and its availability
      for room in list_of_room:
        if list_of_room in list_of_room[room][day].items():
          print(list_of_room)
          return True
      #continue.................
        
  def teacher_availability(self, _course_code, _day, _time):
    available_teachers = []

    # Iterate through teachers
    for teacher in self.teachers:
      if any(_course_code == course['code'] for course in teacher['specialized']): # get the teacher based on specialized course 
        for _, time in self.teacher_availability_dic[teacher['_id']].items():
          time_available = [slot for slot, slotData in time.items() if not slotData]
          if len(time_available) >= len(_time): #validate if the time availability of the teacher is enought to accommodate the course]
            available_teachers.append(teacher['_id'])
          break
          
    return available_teachers

  