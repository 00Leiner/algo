def select_unassigned_course(assignment, list_domain_schedule):
    unassigned_courses = {}
    for (student_id, course_code) in list_domain_schedule:
      if (student_id, course_code) not in assignment:
        return (student_id, course_code)
    return unassigned_courses