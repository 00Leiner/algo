import data
import scheduling

if __name__ == "__main__":
  students = data.students
  courses = data.courses
  teachers = data.teachers
  rooms = data.rooms

  scheduling.Scheduling(students, courses, teachers, rooms)