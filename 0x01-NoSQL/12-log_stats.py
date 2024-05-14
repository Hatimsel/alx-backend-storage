#!/usr/bin/env python3
"""Log stats"""

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    num_of_logs = nginx.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    count = [nginx.count_documents({"method": method}) for method in methods]

    status_check = nginx.count_documents({"path": "/status", "method": "GET"})

    print(f"{num_of_logs} logs")
    print("Methods:")
    for i in range(len(methods)):
        print(f"\tmethod {methods[i]}: {count[i]}")
    print(f"{status_check} status check")
