
````markdown
# 🏫 Thai School Data Toolkit

A set of Python scripts for managing student and teacher data from a Thai school web system. This toolkit includes data extraction, filtering, formatting, and even brute-force OTP testing for internal validation.

---

## 📁 Files Overview

| File | Description |
|------|-------------|
| `bf_otp.py` | Brute-force OTP tester with Discord webhook notifications. |
| `downloads_all.py` | Downloads full student and teacher datasets from the official platform. |
| `filter_student.py` | Organizes and saves student profiles and pictures into a structured folder tree. |
| `filter_teacher.py` | Filters teacher data and downloads profile images into folders by role and name. |

---

## 📦 Requirements

Install the necessary Python packages:

```bash
pip install httpx requests
````

Use Python 3.8 or higher.

---

## 🔐 Brute Force OTP

**File:** `bf_otp.py`

```bash
python bf_otp.py
```

* Randomly generates and submits OTP codes.
* Detects correct OTP by analyzing response.
* Sends a Discord alert via webhook when valid OTP is found.

---

## 📥 Download Raw Student & Teacher Data

**File:** `downloads_all.py`

```bash
python downloads_all.py
```

* Requires valid session cookies (`COOKIE`).
* Saves:

  * `student_raw_data.json`
  * `teacher_raw_data.json`

Make sure to adjust `TERM` and `BODY` if needed.

---

## 🧑‍🎓 Filter Students

**File:** `filter_student.py`

```bash
python filter_student.py
```

* Input: `students_all.json`
* Output:

  * JSON and JPG per student
  * Structured as:
    `alldata_student/levelX/class Y/std_no_name.json`
    `alldata_student/levelX/class Y/std_no_name.jpg`

---

## 👩‍🏫 Filter Teachers

**File:** `filter_teacher.py`

```bash
python filter_teacher.py
```

* Input: `teacher_raw_data.json`
* Output:

  * Each teacher in:
    `alldata_teacher/Position_Name_FullName/{.json + .jpg}`

---

## 🛡️ Disclaimer

> This project is for internal or educational use only.
> Do **not** use these scripts on real-world systems without permission.

---

## 🙋‍♂️ Author

**marioblox** — *The Cyber Sorcerer* 🧙‍♂️
📧 Email: [thatchanajaruphong@gmail.com](mailto:thatchanajaruphong@gmail.com)
📸 IG: [@pers0naxx](https://www.instagram.com/pers0naxx)

> "Clean data is magical data." ✨

````


