import pandas as pd
import webbrowser
import time
import csv
import pyautogui
import tkinter as tk
import threading
import sys

# --- GLOBAL FLAG ---
abort_flag = False
root = None  # Global variable to access Tkinter window

# --- FUNCTION TO SEND WHATSAPP MESSAGES ---
def send_whatsapp_messages():
    global abort_flag

    dataFile = "example.csv"
    waitingDuration = 8
    initialLoadWait = 5

    template = """Bismillah

Punten ngawagel, bade nguningakeun, perihal iuran anggota Pemuda Persis, antum atas nami:

- Nama : {name}           
- NPA : {npa}       

Diantos kanggo iuranna.
Bilih bade bayar anu bulan bulan kapengger oge mangga, tiasa diwaler ka ana bilih bade ninggal iuranna atos sabaraha wae, atanapi bade sakantenan infaq kanggo meringankan anu sanesna mangga ditampi pisan.

Bade janjian dina Jialing wengi ayeuna cash 💰 atanapi di TF 🏧 mangga pisan.

Jazakallah, sing diluaskeun rezekina, digampilkeun sagala urusanna sareng dipasihan kasehatan.
Hatur nuhun"""

    df = pd.read_csv(dataFile, dtype={"npa": str, "phone": str, "status": str})

    if "message" not in df.columns:
        df["message"] = ""

    for index, row in df.iterrows():
        if abort_flag:
            print("🛑 Aborted by user.")
            break

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
        whatsapp_link = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"

        print(f"📨 Opening WhatsApp Web for {name} ({phone})...")
        webbrowser.open(whatsapp_link)

        time.sleep(initialLoadWait)
        pyautogui.press("enter")
        print(f"✅ Message sent to {name}")

        time.sleep(waitingDuration)

        df.at[index, "status"] = "sent"
        print("📂 Saving results to result.csv")
        df.to_csv("result.csv", index=False, quoting=csv.QUOTE_ALL)

    print("🎉 Done sending messages.")
    abort_flag = True
    if root:
        root.destroy()
    sys.exit(0)

# --- TKINTER MAIN THREAD ---
def run_gui():
    def on_abort():
        global abort_flag
        abort_flag = True
        root.destroy()

    global root
    root = tk.Tk()
    root.title("WhatsApp Sender")
    root.geometry("250x100")
    tk.Label(root, text="Sending messages...").pack(pady=5)
    tk.Button(root, text="Abort", fg="white", bg="red", command=on_abort).pack(pady=10)

    # Start message sending in background thread
    threading.Thread(target=send_whatsapp_messages, daemon=True).start()

    root.mainloop()

# Start the GUI in the main thread
if __name__ == "__main__":
    run_gui()