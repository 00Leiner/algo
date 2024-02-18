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
      if day in self.teacher_availability[teacher_id]:
        all_items_true = True
        for t in range(time):
          if t in self.teacher_availability[teacher_id][day]:
            all_items_true = False  # If any item is false, set the flag to False and break out of the loop
            break
        if all_items_true:
          self.teacher_availability[teacher_id][day].append(time)
          return True
        return all_items_true
      else:  #if day is not in the dictionary, add it with the time
        self.teacher_availability[teacher_id].append(day)
        for t in range(time):
          self.teacher_availability[teacher_id][day].append(t)
    else:
      self.teacher_availability[teacher_id][day] = [t for t in range(time)]
      return True
