#!/usr/bin/env python3
"""Change school topics"""


def update_topics(mongo_collection, name, topics):
    """Takes a db coll the school name and a list of topics
    taught int the school
    Updates the coll passed"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
