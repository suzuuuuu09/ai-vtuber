hoge = [
    {"id": 1, "name": "a"}, 
    {"id": 2, "name": "b"}, 
    {"id": 3, "name": "c"},
    {"id": 4, "name": "d"}
]

fuga = [
    {"id": 1, "name": "a"}, 
    {"id": 2, "name": "b"},
    {"id": 5, "name": "e"}
]

diff = [d for d in hoge if d not in fuga]

print(diff)