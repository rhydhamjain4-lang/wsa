import subprocess
import re
import customtkinter as ctk
from tkinter import messagebox


# -----------------------------
# Scan Wi-Fi networks (Windows)
# -----------------------------
def scan_wifi():
    try:
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            encoding="utf-8",
            errors="ignore"
        )

        networks = []

        # Split output into individual networks
        blocks = re.split(r"\n\s*SSID\s+\d+\s*:", result)

        for block in blocks[1:]:
            lines = block.splitlines()

            if not lines:
                continue

            ssid = lines[0].strip()
            security = "Unknown"
            signal = "Unknown"

            for line in lines:
                line = line.strip()

                if line.startswith("Authentication"):
                    security = line.split(":", 1)[1].strip()

                elif line.startswith("Signal"):
                    signal = line.split(":", 1)[1].strip()

            networks.append((ssid, security, signal))

        return networks

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []


# -----------------------------
# Security analysis
# -----------------------------
def analyze_security(security):
    security_lower = security.lower()

    if "open" in security_lower:
        return "HIGH RISK"

    if "wep" in security_lower:
        return "HIGH RISK"

    if "wpa3" in security_lower:
        return "GOOD"

    if "wpa2" in security_lower:
        return "GOOD"

    if "wpa" in security_lower:
        return "MODERATE"

    return "UNKNOWN"


# -----------------------------
# Display networks
# -----------------------------
def start_scan():
    output.delete("1.0", "end")

    output.insert("end", "Scanning nearby Wi-Fi networks...\n\n")

    networks = scan_wifi()

    if not networks:
        output.insert("end", "No networks found.\n")
        return

    output.insert(
        "end",
        f"{'SSID':<25} {'SECURITY':<18} {'SIGNAL':<10} {'RISK'}\n"
    )

    output.insert("end", "-" * 75 + "\n")

    for ssid, security, signal in networks:
        risk = analyze_security(security)

        output.insert(
            "end",
            f"{ssid[:24]:<25} "
            f"{security[:17]:<18} "
            f"{signal:<10} "
            f"{risk}\n"
        )

    output.insert(
        "end",
        "\nScan completed.\n"
    )


# -----------------------------
# Save report
# -----------------------------
def save_report():
    content = output.get("1.0", "end")

    if not content.strip():
        messagebox.showwarning(
            "No Report",
            "Run a Wi-Fi scan first."
        )
        return

    try:
        with open(
            "wifi_security_report.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(content)

        messagebox.showinfo(
            "Saved",
            "Report saved as wifi_security_report.txt"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -----------------------------
# GUI
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("Wi-Fi Security Analyzer")
app.geometry("900x600")
app.resizable(False, False)


# Title
title = ctk.CTkLabel(
    app,
    text="📡 Wi-Fi Security Analyzer",
    font=("Arial", 28, "bold")
)

title.pack(pady=(25, 5))


subtitle = ctk.CTkLabel(
    app,
    text="Ethical Wi-Fi security auditing tool",
    font=("Arial", 15)
)

subtitle.pack(pady=(0, 20))


# Buttons
button_frame = ctk.CTkFrame(app)

button_frame.pack(pady=10)


scan_button = ctk.CTkButton(
    button_frame,
    text="🔍 Scan Networks",
    width=180,
    height=40,
    command=start_scan
)

scan_button.grid(row=0, column=0, padx=10)


save_button = ctk.CTkButton(
    button_frame,
    text="📄 Save Report",
    width=180,
    height=40,
    command=save_report
)

save_button.grid(row=0, column=1, padx=10)


# Output box
output = ctk.CTkTextbox(
    app,
    width=820,
    height=380,
    font=("Consolas", 14)
)

output.pack(pady=20)


# Footer
footer = ctk.CTkLabel(
    app,
    text="Use only on networks you own or have permission to audit.",
    font=("Arial", 12)
)

footer.pack(pady=5)


app.mainloop()