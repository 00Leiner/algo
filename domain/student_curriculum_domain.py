def student_curriculum_domain(students):
        student_curriculum = []

        for student in students:
            student_id = student['_id']
            for course in student['courses']:
                course_code = course['code']
                student_curriculum.append((student_id, course_code))

        return student_curriculum