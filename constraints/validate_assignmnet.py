class validate_assignmnet:
    def __init__(self, teachers_schedule, rooms_schedule, students_schedule, days) -> None:
        self.teachers_schedule = teachers_schedule
        self.rooms_schedule = rooms_schedule
        self.students_schedule = students_schedule
        self.days = days

    def is_assignmnet_valid(self, assignment, student_id, course_code, teacher_id, first_schedule, room_id_for_first_schedule, second_schedule, room_id_for_second_schedule):
        
        if not self.is_teacher_available(teacher_id, first_schedule): #check teacher availability in first schedule
            return False
        if not self.is_teacher_available(teacher_id, second_schedule): #check teacher availability in second schedule
            return False
        if not self.is_room_available(room_id_for_first_schedule, first_schedule):  #check room availability in first schedule
            return False
        if not self.is_room_available(room_id_for_second_schedule, second_schedule): #check room availability in second schedule
            return False
        if not self.is_student_available(student_id, first_schedule): #check teacher availability in first schedule
            return False
        if not self.is_student_available(student_id, second_schedule): #check teacher availability in second schedule
            return False
        
        return True

    def is_teacher_available(self, teacher_id, sched):
        #ensure 1 day rest
        if not self._ensure_teacher_restday(teacher_id, sched):
            return False
        #check if time is available
        if not self._check_teacher_time_availability(teacher_id, sched):
            return False
        # ensure 6 hours maximum a day
        if not self._ensure_6hours_maximum_aday(teacher_id, sched):
            return False
        return True

    def _ensure_teacher_restday(self, teacher_id, sched):
        ensure_rest_day = []
        #get all day that has schedule
        for day in self.teachers_schedule[teacher_id]:
            for time in self.teachers_schedule[teacher_id][day]:
                if self.teachers_schedule[teacher_id][day][time]:
                    ensure_rest_day.append(day)
                    break
        #check if the schedule still have rest
        _day, _ = sched
        if _day not in ensure_rest_day:
            if len(ensure_rest_day) == (len(self.days) - 1):
                return False
            else:
                return True
        else:
            return True
        
    def _ensure_6hours_maximum_aday(self, teacher_id, sched):
        ensure_maximum_of_6hours = []
        _day, _time = sched
        #get all time that has 
        for time in self.teachers_schedule[teacher_id][_day]:
            if self.teachers_schedule[teacher_id][_day][time]:
                ensure_maximum_of_6hours.append(time)
                break
        #check the number of hours the teacher been scheduled
        if len(ensure_maximum_of_6hours) > 6:
            return False

        len_time = len(range(_time[0], _time[1]))
        if (len_time + len(ensure_maximum_of_6hours)) > 6:
            return False
        
        return True
        
    def _check_teacher_time_availability(self, teacher_id, sched):
        check_availability = True
        if sched:
            _day, _time = sched 
            for t in range(_time[0], _time[1] + 1):  # Iterate over the time range
                if self.teachers_schedule[teacher_id][_day][t]:
                    check_availability = False
            return check_availability
        
    def is_room_available(self, room_id, sched):
        check_availability = True
        if sched:
            _day, _time = sched 
            for t in range(_time[0], _time[1]):
                if t in self.rooms_schedule[room_id][_day]:
                    if self.rooms_schedule[room_id][_day][t]:
                        check_availability = False
                        break
                
        return check_availability

    def is_student_available(self, student_id, sched):
        check_availability = True
        if sched:
            _day, _time = sched 
            for t in range(_time[0], _time[1] + 1):
                if t in self.students_schedule[student_id][_day]:
                    if self.students_schedule[student_id][_day][t]:
                        check_availability = False
                        break
        return check_availability

