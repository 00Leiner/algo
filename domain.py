class domain:
  def __init__(self, _room, _day, _time, _courses, _teacher) -> None:
    self.room = _room
    self.time = _time
    self.day = _day
    self.courses = _courses
    self.teacher = _teacher

    self.lab_room_domain()
    self.lec_room_domain()
    self.course_teacher_domain()


  def lab_room_domain(self):
    lab_room = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.room if room['types'] == 'laboratory'}
    return [lab_room]

  def lec_room_domain(self):
    lec_room = {room['_id']: {day: {timeslot: [] for timeslot in self.time} for day in self.day} for room in self.room if room['types'] == 'lecture'}
    return lec_room

  def course_teacher_domain(self):
    list_of_teacher_with_specialized = {course['code']: {teacher['_id'] for teacher in self.teacher if course['code'] in [t['code'] for t in teacher['specialized']]} for course in self.courses}
    return list_of_teacher_with_specialized