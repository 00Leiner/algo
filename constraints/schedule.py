def update_schedule(student_id, teacher_id, room_id, sched, teachers_schedule, students_schedule, rooms_schedule):
    _day, _time = sched
    
    for t in range(_time[0], _time[1]): 
      teachers_schedule[teacher_id][_day][t].append('occupied')
      students_schedule[student_id][_day][t].append('occupied')

    rday = _time[1]# this is for the rest day
    if rday in students_schedule[student_id][_day]:
      students_schedule[student_id][_day][rday].append('rest')
      teachers_schedule[teacher_id][_day][rday].append('rest')
    
    for r in range(_time[0], (_time[1])):
      rooms_schedule[room_id][_day][r].append('occupied')
      
def undo_update_schedule(student_id, teacher_id, room_id, sched, teachers_schedule, students_schedule, rooms_schedule):
    _day, _time = sched

    for t in range(_time[0], _time[1]): 
      teachers_schedule[teacher_id][_day][t].remove('occupied')
      students_schedule[student_id][_day][t].remove('occupied')
    rday = _time[1]
    if rday in students_schedule[student_id][_day]:
      students_schedule[student_id][_day][rday].remove('rest')
      teachers_schedule[teacher_id][_day][rday].remove('rest')

    for r in range(_time[0], (_time[1])):
      rooms_schedule[room_id][_day][r].remove('occupied')
