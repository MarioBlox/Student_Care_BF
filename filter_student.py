import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

with open("students_all.json", "r", encoding="utf-8") as f:
    students = json.load(f)

BASE_DIR = "alldata_student"

def process_student(student):
    try:
        short_name = student.get("classroom_short_name", "")
        if "ม. " not in short_name or "/" not in short_name:
            return
        level, room = short_name.replace("ม. ", "").split("/")
        name_safe = f"{student['std_no']}_{student['prefix_name']}_{student['first_name']}_{student['last_name']}".replace(" ", "_")
        folder = os.path.join(BASE_DIR, f"level{level.strip()}", f"class {room.strip()}", name_safe)
        os.makedirs(folder, exist_ok=True)

        with open(os.path.join(folder, f"{name_safe}.json"), "w", encoding="utf-8") as jf:
            json.dump(student, jf, ensure_ascii=False, indent=2)

        url = student.get("picture_url")
        if url:
            img = requests.get(url, timeout=10).content
            with open(os.path.join(folder, f"{name_safe}.jpg"), "wb") as f:
                f.write(img)
    except Exception as e:
        print("❌", e)

with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(process_student, students)
