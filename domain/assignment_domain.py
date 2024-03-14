class assignmnet_domain:
    def __init__(self, student_curriculum, teachers, course_type, rooms, days, timeslots):
        self.student_curriculum = student_curriculum
        self.teachers = teachers
        self.course_type = course_type
        self.rooms = rooms
        self.days = days
        self.timeslots = timeslots
        
    def assignment_domain(self):
        domain_schedule = {}
        
        for student_id, course_code in self.student_curriculum:

            domain_schedule[(student_id,course_code)] = {
                'teacher': None,
                'schedule': {
                    'first': None,
                    'first_day_room': None,
                    'second': None,
                    'second_day_room': None
                }
            }

            teachers_for_course = [
                teacher['_id'] for teacher in self.teachers
                if course_code in [t['code'] for t in teacher['specialized']]
            ]
        
            course_type = self.course_type[course_code]
            rooms_for_first_day = self.room_assignment(course_type)

            rooms_for_second_day = self.room_assignment('lecture')

            first_sched = self.first_day_schedule(course_code)

            second_sched = {}
            for _day, _ in first_sched:
                second_sched = self.second_day_schedule(course_code, _day)

            domain_schedule[(student_id,course_code)]['teacher'] = teachers_for_course
            domain_schedule[(student_id,course_code)]['schedule']['first'] = first_sched
            domain_schedule[(student_id,course_code)]['schedule']['first_day_room'] = rooms_for_first_day
            domain_schedule[(student_id,course_code)]['schedule']['second'] = second_sched
            domain_schedule[(student_id,course_code)]['schedule']['second_day_room'] = rooms_for_second_day

        return domain_schedule

    def room_assignment(self, course_type):
        set_of_room = []
        for room in self.rooms:
            if room['types'] == course_type:
                set_of_room.append(room['_id'])
                return room['_id']

    def first_day_schedule(self, course_code):
        type = self.course_type[course_code]
        list_of_timeslots = list(self.timeslots)
        time_schedule = []
        if type == 'laboratory':
            #3 hours in laboratory
            for day in self.days:
                for i in range(len(list_of_timeslots) - 3):
                    set_of_3 = (day, (list_of_timeslots[i], list_of_timeslots[i + 3]))
                    time_schedule.append(set_of_3)
        
        if type == 'lecture':
            #3 hours in lecture
            for day in self.days:
                for i in range(len(list_of_timeslots) - 2):
                    set_of_2 = (day, (list_of_timeslots[i], list_of_timeslots[i + 2]))
                    time_schedule.append(set_of_2)
                    
        return time_schedule

    def second_day_schedule(self, course_code, first_day):
        type = self.course_type[course_code]
        list_of_timeslots = list(self.timeslots)
        list_of_days = list(self.days)

        #2 days gap from first schedule
        first_day_index = list_of_days.index(first_day)
        second_day_index = (first_day_index + 4) % len(list_of_days)
        second_day = list_of_days[second_day_index]

        if type == 'laboratory':
            # 2 hours in lecture
            sets_of_time_in_lecture = []
            for i in range(len(list_of_timeslots) - 2):
                _timeslot = (second_day, (list_of_timeslots[i], list_of_timeslots[i + 2]))
                sets_of_time_in_lecture.append(_timeslot)
            return sets_of_time_in_lecture

        if type == 'lecture':
            # 2 hours in lecture
            sets_of_time_in_lecture = []
            for i in range(len(list_of_timeslots) - 1):
                _timeslot = (second_day, (list_of_timeslots[i], list_of_timeslots[i + 1]))
                sets_of_time_in_lecture.append(_timeslot)

            return sets_of_time_in_lecture
