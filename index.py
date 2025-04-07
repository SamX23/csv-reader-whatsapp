import pandas as pd
import webbrowser
import time
import csv
import pyautogui

# variables
dataFile = "example.csv"
waitingDuration = 8  # Total wait time before sending message
initialLoadWait = 5  # Time to wait after opening the link before sending ENTER
# Message template
template = """Bismillah

Punten ngawagel, bade nguningakeun, perihal iuran anggota Pemuda Persis, antum atas nami:

- Nama : {name}           
- NPA : {npa}       

Diantos kanggo iuranna.
Bilih bade bayar anu bulan bulan kapengger oge mangga, tiasa diwaler ka ana bilih bade ninggal iuranna atos sabaraha wae, atanapi bade sakantenan infaq kanggo meringankan anu sanesna mangga ditampi pisan.

Bade janjian dina Jialing wengi ayeuna cash 💰 atanapi di TF 🏧 mangga pisan.

Jazakallah, sing diluaskeun rezekina, digampilkeun sagala urusanna sareng dipasihan kasehatan.
Hatur nuhun"""

# Load CSV
df = pd.read_csv(dataFile, dtype={"npa": str, "phone": str, "status": str})

if "message" not in df.columns:
    df["message"] = ""

for index, row in df.iterrows():
    if row["status"] in ["sent", "skip"]:
        continue

    name = row["name"]
    npa = row["npa"]
    phone = str(row["phone"]).strip()

    if not phone or phone == "nan":
        print(f"❌ Skipping {name}: No phone number")
        continue

    message = template.format(name=name, npa=npa)
    df.at[index, "message"] = message

    encoded_message = message.replace(" ", "%20").replace("\n", "%0A")
    whatsapp_link = f"https://wa.me/{phone}?text={encoded_message}"

    print(f"📨 Opening WhatsApp link for {name} ({phone})...")
    webbrowser.open(whatsapp_link)

    # Wait for the page to load (tweak this value as needed)
    time.sleep(initialLoadWait)

    # pyautogui.alert("Sending message... Please do not touch mouse or keyboard")

    # Press Enter to send message
    pyautogui.press("enter")
    print(f"✅ Message sent to {name}")

    time.sleep(waitingDuration)  # wait before processing next

    df.at[index, "status"] = "sent"
    df.to_csv("result.csv", index=False, quoting=csv.QUOTE_ALL)

print("🎉 All messages sent and status updated!")
