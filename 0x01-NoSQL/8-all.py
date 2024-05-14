#!/usr/bin/env python3
"""list all documents in python"""

from pymongo import MongoClient


def list_all(mongo_collection):
    """"
    Takes a collection
    Lists all docs in the collection
    Returns an empty list if no doc in the coll"""
    result = mongo_collection.find()

    return result
