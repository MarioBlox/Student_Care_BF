import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

# โหลดข้อมูลจาก key "rows"
with open("teacher_raw_data.json", "r", encoding="utf-8") as f:
    raw = json.load(f)
    teachers = raw.get("rows", [])

print("จำนวนครูทั้งหมด:", len(teachers))

BASE_DIR = "alldata_teacher"

def process_teacher(t):
    try:
        pos = (t.get("POSITION_NAME") or "ไม่ระบุตำแหน่ง").strip().replace(" ", "_")
        name = (t.get("NAME") or "ไม่ระบุชื่อ").strip().replace(" ", "_")

        folder_name = f"{pos}_{name}"
        folder_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        with open(os.path.join(folder_path, f"{folder_name}.json"), "w", encoding="utf-8") as jf:
            json.dump(t, jf, ensure_ascii=False, indent=2)

        teacher_id = t.get("TEACHER_ID")
        if teacher_id:
            url = f"https://webapp.student.co.th/application/uploads/institues_teacher_picture/{teacher_id}.jpg?t=1150"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(os.path.join(folder_path, f"{folder_name}.jpg"), "wb") as imgf:
                    imgf.write(response.content)
            else:
                print(f"❌ ไม่มีรูป: {teacher_id}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(process_teacher, teachers)

print("✅ เสร็จสิ้น")
