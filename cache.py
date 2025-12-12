import json, os, datetime

os.chdir(r"C:\Users\HP\Desktop\Project\Inventory and Billing Management System")

CACHE_FILE = "billing/cache.json"

class Cache:
    def __init__(self, username, action, cache_data):
        if self.cache_check(username):
            self.overwrite_cache(username, action, cache_data)
            return
        self.write_cache(username, action, cache_data)

    def undo(self, username):
        pass     

    @staticmethod
    def _load_cache_file():
        if not os.path.exists(CACHE_FILE):
            return []
    
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def cache_check(self, username):
        data = self._load_cache_file()

        if data["username"] == username:
            return True
        return False
    
    def overwrite_cache(self, username, action, cache_data):
        data = self._load_cache_file()

        for u in data:
            if u["username"] == username:
                data["action"] == action
                data["cache_data"] = cache_data
                data["updated"] = str(datetime.datetime.now())
                
                with open(CACHE_FILE, 'w') as f:
                    json.dump(data, f, indent=4)
                
                return

    def write_cache(self, username, action, cache_data):
        data = self._load_cache_file()

        new_cache = {
            "username": username,
            "action": action,
            "cache_data": cache_data,
            "created": str(datetime.datetime.now()),
            "updated": None,
        }

        data.append(new_cache)

        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        return