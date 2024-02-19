class Teacher:

  def __init__(self, teachers, max_daily_hours, max_continuous_hours,
               max_day_in_week):
    self.teachers = teachers
    self.max_daily_hours = max_daily_hours
    self.max_continuous_hours = max_continuous_hours
    self.max_day_in_week = max_day_in_week
    self.teacher_availability = {}
    #print(self.teachers)

  def teacher_constraints(self, teacher_id, day, time):
    if teacher_id in self.teacher_availability:
      if self.rest_day(teacher_id) == True: #if teacher is available on the day
        if day in self.teacher_availability[teacher_id]:
          if self.six_hours_per_day(self, teacher_id, day) == True: #if teacher is available within the day
            if self.continuous_hours(self, teacher_id, day, time) == True: #if teacher is available within
              return True
            else:
              return False 
        else:  #if day is not in the dictionary, add it with the time
          self.teacher_availability[teacher_id].append(day)
          for t in range(time):
            self.teacher_availability[teacher_id][day].append(t)
    else:
      self.teacher_availability[teacher_id][day] = [t for t in range(time)]
      return True

  def rest_day(self, teacher_id):
    if self.max_day_in_week == len(self.teacher_availability[teacher_id]):
      return False
    else:
      return True

  def six_hours_per_day(self, teacher_id, day):
    if self.max_daily_hours == len(self.teacher_availability[teacher_id][day]):
      return False
    else:
      return True

  def continuous_hours(self, teacher_id, day, time):
    all_items_true = True
    for t in range(time): #(start, end)
      if t in self.teacher_availability[teacher_id][day]:
        all_items_true = False  # If any item is false, set the flag to False and break out of the loop
        break
    if all_items_true:
      self.teacher_availability[teacher_id][day].append(time)
      return True