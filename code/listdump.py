import json
with(open("dumpedlist.json","w")) as out:
    out.write(json.dumps(range(1,10000)))