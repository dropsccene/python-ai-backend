import json
import csv
def append_task_to_file(task:dict,filepath:str):
    with open(filepath,'a') as f:
        f.write(f"{task}\n")

append_task_to_file({"id":"4","title":"遛狗","done":False},"tasks.json")

def save_tasks_as_json(tasks:list[dict],filepath:str)-> None:
    json_str = json.dumps(tasks,indent=2,ensure_ascii=False)
    with open(filepath,'w') as f:
        f.write(json_str)

save_tasks_as_json([{"id":"1","title":"喝牛奶","done":False},
                    {"id":"2","title":"写作业","done":False},
                    {"id":"3","title":"倒垃圾","done":False}
                    ],"tasks.json")

def load_tasks_from_json(filepath:str) -> list[dict]:
    with open(filepath,'r') as f:
        return json.load(f)
print(load_tasks_from_json("tasks.json"))

def save_tasks_as_csv(tasks:list[dict],filepath:str) -> None:
    with open(filepath,'w') as f:
        fieldnames = ["id","title","done"]
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)


def load_tasks_from_csv(filepath:str) -> list[dict]:
    tasks = []
    with open(filepath,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append(row)
    return tasks

test_tasks = [{"id":"1","title":"喝牛奶","done":"False"},{"id":"2","title":"写作业","done":"False"}]

save_tasks_as_csv(test_tasks,"tasks.csv")
loaded_tasks = load_tasks_from_csv("tasks.csv")
print("原始:",test_tasks)
print("加载:",loaded_tasks)