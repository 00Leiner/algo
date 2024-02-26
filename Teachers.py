class Teacher:

  def __init__(self, teachers, max_daily_hours, max_continuous_hours, max_day_in_week):
    self.teachers = teachers
    self.max_daily_hours = max_daily_hours
    self.max_continuous_hours = max_continuous_hours
    self.max_day_in_week = max_day_in_week
    self.teacher_availability = {}
    #print(self.teachers)

  def teacher_constraints(self, teacher_id, day, time):
    if teacher_id in self.teacher_availability:
      if self.rest_day_required(
          teacher_id):  #1 day rest within weekly working days
        if day in self.teacher_availability[teacher_id]:
          if self.check_working_hour_limit(self, teacher_id,day):  #6 hours daily hourly limit
            if self.check_time_availability(teacher_id, day, time):
              if self.rest_hour_required(self, teacher_id, day, time):  #required rest hour
                for start, end in time:
                  self.teacher_availability[teacher_id][day].append((start, end))
                return True
              else:
                return False
            else:
              return False
          else:
            return False
        else:  #if day is not in the dictionary, add it with the time
          self.teacher_availability[teacher_id].append(day)
          for start, end in time:
            self.teacher_availability[teacher_id][day].append((start, end))
      else:
        return False
    else:  #if teacher is not in the dictionary, add it with the day and time
      self.teacher_availability.append([teacher_id][day] = [(start, end) for start, end in time])
      return True

  def rest_day_required(self, teacher_id):
    if self.max_day_in_week == len(self.teacher_availability[teacher_id]):
      return False
    else:
      return True

  def check_working_hour_limit(self, teacher_id, day):
    if self.max_daily_hours == len(self.teacher_availability[teacher_id][day]):
      return False
    else:
      return True

  def check_time_availability(self, teacher_id, day, time):
    availability_on_day = self.teacher_availability[teacher_id][day]
    check = True
    for start, end in time:
      if (start, end) in availability_on_day:
        check = False
        break
    return check

  def rest_hour_required(self, teacher_id, day, time):
    combination = self.teacher_availability[teacher_id][day] + time
    sorted_time = sorted(combination, key=lambda x: x[0])
    if self.check_time_schedule(sorted_time):
      return False
    else:
      return True

  def check_time_schedule(self, time):
    check = True
    for i in range(len(time) - 3):
      start_times = [slot[0] for slot in time[i:i + 4]]
      end_times = [slot[1] for slot in time[i:i + 4]]
      if start_times == [
          start_times[0] + j for j in range(4)
      ] and end_times == [end_times[0] + j for j in range(4)]:
        check = False
    return check
