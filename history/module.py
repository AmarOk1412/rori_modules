from rori import RORIData
from history import DBManager
import sys

# TODO, in the future, RORI will have to do this in Rust
if len(sys.argv) == 5:
    author = sys.argv[1][1:-1]
    content = sys.argv[2][1:-1]
    client = sys.argv[3][1:-1]
    datatype = sys.argv[4][1:-1]
    data = RORIData(author=author, content=content, client=client, datatype=datatype)
    db = DBManager()
    db.store_data(data.author, data.content, data.client, data.datatype)
else:
    print("usage: python3 module.py author content client datatype")
