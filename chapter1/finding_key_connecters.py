from __future__ import division  # integer division is lame

users = [  # list
    {"id": 0, "name": "Hero"},  # dict
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"}
]
friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# add a list of firends to each user
for user in users:
    user["friends"] = []
for i, j in friendships:
    users[i]["friends"].append(users[j])  # the list index corresponds to id number
    users[j]["friends"].append(users[i])


def number_of_firends(user):
    """how many firends does _user_ habe?"""
    return len(user["friends"])


total_connections = sum(number_of_firends(user) for user in users)

number_users = len(users)
avg_connections = total_connections / number_users
print(avg_connections)

# create a list (user_id,number_of_friends)
num_friends_by_id = [(user["id"], number_of_firends(user)) for user in users]

# sorted(num_friends_by_id, key=lambda  user_id,num_friends: num_friends, reverse=True)
# there is something wrong in the just above line code

# for i in num_friends_by_id:
#     print(i)
