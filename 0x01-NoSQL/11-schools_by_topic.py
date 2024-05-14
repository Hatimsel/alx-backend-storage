#!/usr/bin/env python3
"""Where can I learn Python"""


def schools_by_topic(mongo_collection, topic):
    """Takes a db coll, and a topic
    Returns the docs with that topic"""

    result = mongo_collection.find({"topics": topic})

    return result
