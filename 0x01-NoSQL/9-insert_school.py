#!/usr/bin/env python3
"""Insert a document in python"""


def insert_school(mongo_collection, **kwargs):
    """Takes a db coll, and keyword args
    inserts the new obj into the db
    Returns the new _id"""
    inserted_obj = mongo_collection.insert_one(kwargs)

    return inserted_obj.inserted_id
