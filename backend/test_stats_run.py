import sys
from database.mongodb import MongoDB

try:
    db = MongoDB()
    print("Initial stats:")
    stats = db.get_stats()
    print("Stats result:", stats)
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
