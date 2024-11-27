import os


path = "D:\\test"

for name in os.listdir(path):
    p = os.path.join(path, name)
    f = open(p, encoding="utf-8")
    s = ""
    line = f.readline()
    while line:
        s += line
        line = f.readline()
    s = s.split('<')[1:]
    for t in range(len(s)):
        s[t] = s[t].split(">")[0]
        s[t] = s[t].split("\t")[0]
    print(s)