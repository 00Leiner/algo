class Scheduling:

  def __init__(self, _students, _courses, _teachers, _rooms):
    #variable
    self.students = _students
    self.teachers = _teachers
    self.courses = _courses
    self.rooms = _rooms
    self.day = ["Monday", "Tuesday", "Wednesday", 'Thuesday']
    self.time = [(7, 8), (8, 9),(9,10),(10,11),(12,13), (13,14)]

    #dictionry for domain
    self.lab_room_schedule = {} # laboratory room availability 
    self.lec_room_schedule = {} # lecture room availability 
    self.teacher_schedule = {} # teacher availability
    self.student_schedule = {} # student availability
    
    #initialization 
    self.initialize()
    
  def initialize(self): 
    self.domain()
    self.assignment()
    
  def domain(self):
    self.lab_room_schedule = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.rooms if room['types'] == 'laboratory'}
    
    self.lec_room_schedule = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.rooms if room['types'] == 'lecture'}

    self.teacher_schedule = {teacher['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for teacher in self.teachers}

    self.student_schedule = {student['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for student in self.students}
    
    self.list_of_available_teacher_in_course = {course['code']: {teacher['_id'] for teacher in self.teachers if course['code'] in [t['code'] for t in teacher['specialized']]} for course in self.courses}

  def assignment(self):
    for student in self.students:
      student_id = student['_id']
      for course in student['courses']:
        course_type = course['types']
        course_id = course['code']

        if course_type == 'laboratory':
          #vaiable
          hrsInLab = 3
          hrsInLec = 2
          laboratory_room = self.lab_room_schedule
          
          availability_of_student = self.student_availability(student_id, hrsInLab, 0)
          #first day schedule
          for first_day, timeslot_in_1stday in availability_of_student.items():
            if timeslot_in_1stday: #check if empty
              for set_of_hrsInLab in timeslot_in_1stday:
                teacher_available_1stday = self.teacher_availability(course_id, first_day, set_of_hrsInLab, 0)
                if teacher_available_1stday:
                  is_room_available_in_1stday = self.room_availability(laboratory_room, first_day, set_of_hrsInLab)
                  if is_room_available_in_1stday:
                    
                    #second day schedule
                    second_day = self.second_day_schedule(first_day)
                    availability_of_student_for_second_schedule = self.student_availability(student_id, hrsInLec, second_day)
                    for second_day, timeslot_in_2ndday in availability_of_student_for_second_schedule.items():
                      if timeslot_in_2ndday:
                        for set_of_hrsInLac in timeslot_in_2ndday:
                          teacher_available_2ndday = self.teacher_availability(0, second_day, set_of_hrsInLac, teacher_available_1stday)
                          if teacher_available_2ndday:
                            room_available_for_2ndday = self.room_availability(laboratory_room, second_day, set_of_hrsInLac) 
                            if room_available_for_2ndday:
                              pass #set the teacher, room, student schedule
                    
                #for secondday of the lab should be schedule in lecture room
                # if lab is monday the lec should be schedule on thursday

  def student_availability(self, student_id, NumOfHrs, _day):
    available_slots = {}
    if not _day:
      for day, time in self.student_schedule[student_id].items():
        available_indices = [(time_slot, slotData) for time_slot, slotData in time.items()] #get the available time slot to manage the consecutivity of time slot
        available_slots[day] = []  
        for i in range(len(available_indices) - (NumOfHrs - 1)): # loop for respect the number of hours requirements
          set_indices = available_indices[i:i + NumOfHrs] #setting the consecutive time slot for the number of hours requirements
          if all(not slotData for _, slotData in set_indices):  #eliminating the set of time slot that is already occupied 
            available_slots[day].append([slot for slot, _ in set_indices])
    else:
      if _day in self.student_schedule[student_id]:
        available_indices = [(time_slot, slotData) for time_slot, slotData in self.student_schedule[student_id][_day].items()]#get the available time slot to manage the consecutivity of time slot
        available_slots[_day] = []  
        for i in range(len(available_indices) - (NumOfHrs - 1)): # loop for respect the number of hours requirements
          set_indices = available_indices[i:i + NumOfHrs] #setting the consecutive time slot for the number of hours requirements
          if all(not slotData for _, slotData in set_indices): #eliminating the set of time slot that is already occupied  
            available_slots[_day].append([slot for slot, _ in set_indices])
            
    return available_slots
                       
  def room_availability(self, list_of_room, _day, setOfTime):
    for room, days in list_of_room.items():
      for day, timeData in days.items():
        if day == _day:  # getting the day in the room 
          list_of_available = [time for time, slotData in timeData.items() if not slotData] # eliminating the time slot that is already occupied within the day
          if all(pertime in list_of_available for pertime in setOfTime): # is set of time slot is available in the day return true
            return True  
            
    return False  # No match found for the specified day and set of times
        
  def teacher_availability(self, _course_code, _day, _time, teacher_id):
    available_teachers = []

    if _course_code:
      for teacher in self.teachers:
        if any(_course_code == course['code'] for course in teacher['specialized']): # get the teacher based on specialized course 
          for _, time in self.teacher_schedule[teacher['_id']].items():
            time_available = [slot for slot, slotData in time.items() if not slotData]
            if len(time_available) >= len(_time): #validate if the time availability of the teacher is enought to accommodate the course] 
              if all(pertime in time_available for pertime in _time):
                available_teachers.append(teacher['_id'])
                break

    #double check the teacher availability -------------
    if teacher_id:
      for _, time in self.teacher_schedule[teacher_id].items():
        time_available = [slot for slot, slotData in time.items() if not slotData]
        if len(time_available) >= len(_time): #validate if the time availability of the teacher is enought to accommodate the course] 
          if all(pertime in time_available for pertime in _time):
            available_teachers.append(teacher_id)
            break

        #else break
            
    return available_teachers

  def second_day_schedule(self, _day):
    first_day_index = self.day.index(_day)
    second_day_index = (first_day_index + 2) % len(self.day)
    second_day = self.day[second_day_index]
    return second_day
    
    
    
    
      
      