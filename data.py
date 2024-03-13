courses = [{
    "_id": "1",
    "code": "cs1",
    "description": "cs1des",
    "units": "3",
    "types": "laboratory"
}, {
    "_id": "2",
    "code": "cs2",
    "description": "cs2des",
    "units": "3",
    "types": "lecture"
}]

rooms = [{
    "_id": "1",
    "name": "room1",
    "types": "laboratory"
},{
             "_id": "3",
             "name": "room3",
             "types": "laboratory"
         }, {
              "_id": "4",
              "name": "room4",
              "types": "laboratory"
          },{
    "_id": "2",
    "name": "room2",
    "types": "lecture"
}]

students = [{
    "_id":
    "1",
    "program":
    "BSCS",
    "year":
    "4",
    "semester":
    "1",
    "block":
    "A",
    "courses": [{
      "_id": "1",
      "code": "cs1",
      "description": "cs1des",
      "units": "3",
      "types": "laboratory"
    }, {
                   "_id": "2",
                   "code": "cs2",
                   "description": "cs2des",
                   "units": "3",
                   "types": "laboratory"
               }]
}]

teachers = [{
    "_id":
    "1",
    "name":
    "teacher1",
    "specialized": [{
        "_id": "1",
        "code": "cs1",
        "description": "cs1des",
        "units": "3",
        "types": "laboratory"
    }, {
        "_id": "2",
        "code": "cs2",
        "description": "cs2des",
        "units": "3",
        "types": "lecture"
    }]
},{
  "_id":"2",
  "name":"teacher2",
  "specialized": [{
                   "_id": "2",
                   "code": "cs2",
                   "description": "cs2des",
                   "units": "3",
                   "types": "lecture"
               }]
           },{
  "_id":"3",
  "name":"teacher3",
  "specialized": [{
    "_id": "1",
    "code": "cs1",
    "description": "cs1des",
    "units": "3",
    "types": "laboratory"
                        }]
                    }]
