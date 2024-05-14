#!/usr/bin/env python3
"""Top students"""


def top_students(mongo_collection):
    """Takes a db collection
    Returns students sorted by average score"""
    pipeline = [
            {
                "$unwind": "$topics"
            },
            {
                "$group": {
                    "_id": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
            },
            {
                "$sort": {"averageScore": -1}
            },
            {
                "$project": {
                    "_id": 1,
                    "name": "$_id",
                    "averageScore": 1
                }
            }
    ]
    return list(mongo_collection.aggregate(pipeline))

# list_all = __import__('8-all').list_all


# def top_students(mongo_collection):
#     """Takes a db collection
#     Returns students sorted by average score"""
#     students = list_all(mongo_collection)

#     for student in students:
#         topics = student.get('topics')
#         scores = [topic.get('score') for topic in topics]
#         average_score = sum(scores) / len(scores)

#         mongo_collection.update_many(
#                 {"name": student.get('name')},
#                 {"$set": {"averageScore": average_score}}
#                 )

#     return mongo_collection.find().sort({"averageScore": -1})
