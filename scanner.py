# scanner.py
import subprocess
import magic
import hashlib
import os
import requests
from config import VIRUSTOTAL_API_KEY

def scan_file(file_path):
    # Fayl turi
    file_type = magic.from_file(file_path, mime=True)

    # Hash hisoblash
    with open(file_path, "rb") as f:
        data = f.read()
        file_hash = hashlib.sha256(data).hexdigest()

    # ClamAV orqali tekshirish
    result = subprocess.run(["clamscan", file_path], capture_output=True, text=True)

    if "OK" in result.stdout:
        virus_status = "✅ Xavfsiz"
    else:
        virus_status = "⚠️ Virus aniqlangan!"

    vt_result = None
    if VIRUSTOTAL_API_KEY:
        vt_result = check_virustotal(file_hash)

    return {
        "file_type": file_type,
        "hash": file_hash,
        "virus_status": virus_status,
        "clamav_output": result.stdout,
        "virustotal": vt_result
    }

def check_virustotal(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]
            return f"VirusTotal natijasi: 🔍 {stats['malicious']} zararli, {stats['undetected']} xavfsiz"
        else:
            return f"VirusTotal javobi: {r.status_code}"
    except Exception as e:
        return f"VirusTotal xatosi: {e}"
