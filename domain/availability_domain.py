def teacher_availability_domain(teachers, days, timeslots):
    teachers_schedule = {
        teacher['_id']: {
            day: {
                time: []
                for time in timeslots
            }
            for day in days
        }
        for teacher in teachers
    }
    return teachers_schedule

def student_availability_domain(students, days, timeslots):
    students_schedule = {
        student['_id']: {
            day: {
                time: []
                for time in timeslots
            }
            for day in days
        }
        for student in students
    }
    return students_schedule

def room_availability_domain(rooms, days, timeslots):
    rooms_schedule = {
        room['_id']: {
            day: {
                time: []
                for time in timeslots
            }
            for day in days
        }
        for room in rooms
    }
    return rooms_schedule
