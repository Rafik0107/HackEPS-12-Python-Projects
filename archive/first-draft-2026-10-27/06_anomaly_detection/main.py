import json
from src.project import demo

if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, ensure_ascii=False))
