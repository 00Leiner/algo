import data
import scheduling
import csp
from flask import Flask, jsonify


if __name__ == "__main__":
  students = data.students
  courses = data.courses
  teachers = data.teachers
  rooms = data.rooms

  #scheduling.Scheduling(students, courses, teachers, rooms)
  csp.CSPAlgorithm(students, courses, teachers, rooms)