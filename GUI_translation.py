from tkinter import *
from translation_base import *

# ---------- Constants ----------
LANGUAGES = [
    "Persian",
    "English",
    "Spanish",
    "Arabic",
    "Japanese",
    "Russian",
    "Chinese",
    "German",
    "Italian",
]

SYMBOLS = ["fa", "en", "es", "ar", "ja", "ru", "zh", "de", "it"]

FLAGS = ["🇮🇷", "🇬🇧", "🇪🇸", "🇸🇦", "🇯🇵", "🇷🇺", "🇨🇳", "🇩🇪", "🇮🇹"]

# ---------- Color Palette ----------
COLORS = {
    "bg": "#1a1a2e",
    "bg_secondary": "#16213e",
    "accent": "#e94560",
    "accent_hover": "#ff6b81",
    "text": "#eeeeee",
    "text_secondary": "#a8a8b3",
    "entry_bg": "#0f3460",
    "list_bg": "#0f3460",
    "list_alt": "#1a1a40",
    "copy": "#0f3460",
    "copy_hover": "#1a4a7a",
}


def enter():
    input_text = input_entry.get().strip()

    if not input_text:
        output_label.config(
            fg=COLORS["accent"], text="⚠️ Please enter text to translate"
        )
        return

    # ---------- Source ----------
    selected_input = input_list.curselection()
    source = SYMBOLS[selected_input[0]] if selected_input else "en"

    # ---------- Target ----------
    selected_output = output_list.curselection()
    target = SYMBOLS[selected_output[0]] if selected_output else "fa"

    # ---------- RTL Support ----------
    if target in ["fa", "ar"]:
        output_label.config(anchor="ne", justify="right")
    else:
        output_label.config(anchor="nw", justify="left")

    output_label.config(fg=COLORS["text"], text="⏳ Translating...")

    data = create_data(src=source, tgt=target, txt=input_text)
    url, header = url_header()
    response = sending_request(data, url=url, header=header)

    if not response:
        output_label.config(fg=COLORS["accent"], text="❌ Error! Please try again")
    else:
        output_label.config(fg=COLORS["text"], text=response)


def copy_text():
    text = output_label.cget("text")
    if text and text not in [
        "⏳ Translating...",
        "⚠️ Please enter text to translate",
        "❌ Error! Please try again",
    ]:
        window.clipboard_clear()
        window.clipboard_append(text)
        window.update()
        copy_button.config(text="✅ Copied!", bg=COLORS["accent"])
        window.after(
            1500, lambda: copy_button.config(text="📋 Copy", bg=COLORS["copy"])
        )


def update_indicators(*args):
    src_idx = input_list.curselection()
    tgt_idx = output_list.curselection()

    src_name = LANGUAGES[src_idx[0]] if src_idx else "English"
    tgt_name = LANGUAGES[tgt_idx[0]] if tgt_idx else "Persian"

    src_flag = FLAGS[src_idx[0]] if src_idx else "🇬🇧"
    tgt_flag = FLAGS[tgt_idx[0]] if tgt_idx else "🇮🇷"

    source_indicator.config(text=f"{src_flag} Source: {src_name}")
    target_indicator.config(text=f"{tgt_flag} Target: {tgt_name}")


# ---------- Window Setup ----------
window = Tk()
window.title("✨ Kamyar Translator")
window.geometry("800x540")
window.configure(bg=COLORS["bg"])
window.resizable(False, False)

# ---------- Icon ----------
try:
    p1 = PhotoImage(
        file="C:\\Users\\ASUS\\Desktop\\Kamyar Documents\\coding\\python\\translation\\icon.png"
    )
    window.iconphoto(False, p1)
    window.iconbitmap("icon.ico")
except:
    pass

# ========== TOP SECTION ==========
# ---------- Title ----------
title_label = Label(
    window,
    text="🌍 Kamyar Translator",
    font=("Helvetica", 26, "bold"),
    bg=COLORS["bg"],
    fg=COLORS["text"],
)
title_label.place(x=30, y=20, anchor="w")

subtitle_label = Label(
    window,
    text="Translate between 9 languages seamlessly • Select source & target from lists",
    font=("Helvetica", 10),
    bg=COLORS["bg"],
    fg=COLORS["text_secondary"],
)
subtitle_label.place(x=30, y=50, anchor="w")

# ========== MIDDLE SECTION - INPUT & BUTTONS ==========
# ---------- Input Box ----------
input_label = Label(
    window,
    text="📝 Enter text to translate",
    font=("Helvetica", 11, "bold"),
    bg=COLORS["bg"],
    fg=COLORS["text"],
)
input_label.place(x=30, y=90, anchor="w")

input_entry = Entry(
    window,
    width=38,
    font=("Helvetica", 13),
    bg=COLORS["entry_bg"],
    fg=COLORS["text"],
    insertbackground=COLORS["text"],
    relief="flat",
    highlightthickness=2,
    highlightcolor=COLORS["accent"],
    highlightbackground=COLORS["bg_secondary"],
)
input_entry.place(x=30, y=115, anchor="w")

# ---------- Source Language List (compact) ----------
input_list_label = Label(
    window,
    text="From :",
    font=("Helvetica", 10, "bold"),
    bg=COLORS["bg"],
    fg=COLORS["text_secondary"],
)
input_list_label.place(x=510, y=45, anchor="w")

input_list = Listbox(
    window,
    width=13,
    height=6,
    bg=COLORS["list_bg"],
    fg=COLORS["text"],
    selectbackground=COLORS["accent"],
    selectforeground=COLORS["text"],
    activestyle="none",
    exportselection=False,
    relief="flat",
    font=("Helvetica", 9),
)
for i, name in enumerate(LANGUAGES):
    input_list.insert(END, f"{FLAGS[i]} {name}")
    input_list.itemconfig(i, bg=COLORS["list_bg"] if i % 2 == 0 else COLORS["list_alt"])
input_list.place(x=510, y=110, anchor="w")
input_list.selection_set(1)

# ---------- Target Language List (compact) ----------
output_list_label = Label(
    window,
    text="To :",
    font=("Helvetica", 10, "bold"),
    bg=COLORS["bg"],
    fg=COLORS["text_secondary"],
)
output_list_label.place(x=660, y=45, anchor="w")

output_list = Listbox(
    window,
    width=13,
    height=6,
    bg=COLORS["list_bg"],
    fg=COLORS["text"],
    selectbackground=COLORS["accent"],
    selectforeground=COLORS["text"],
    activestyle="none",
    exportselection=False,
    relief="flat",
    font=("Helvetica", 9),
)
for i, name in enumerate(LANGUAGES):
    output_list.insert(END, f"{FLAGS[i]} {name}")
    output_list.itemconfig(
        i, bg=COLORS["list_bg"] if i % 2 == 0 else COLORS["list_alt"]
    )
output_list.place(x=660, y=110, anchor="w")
output_list.selection_set(0)

# ---------- Buttons ----------
button_frame = Frame(window, bg=COLORS["bg"])
button_frame.place(x=30, y=175, anchor="w")

submit_button = Button(
    button_frame,
    text="🔄 Translate",
    font=("Helvetica", 14, "bold"),
    bg=COLORS["accent"],
    fg=COLORS["text"],
    activebackground=COLORS["accent_hover"],
    activeforeground=COLORS["text"],
    relief="flat",
    padx=25,
    pady=8,
    cursor="hand2",
    command=enter,
)
submit_button.pack(side=LEFT, padx=(0, 12))

copy_button = Button(
    button_frame,
    text="📋 Copy",
    font=("Helvetica", 14, "bold"),
    bg=COLORS["copy"],
    fg=COLORS["text"],
    activebackground=COLORS["copy_hover"],
    activeforeground=COLORS["text"],
    relief="flat",
    padx=25,
    pady=8,
    cursor="hand2",
    command=copy_text,
)
copy_button.pack(side=LEFT)

# ---------- Quick shortcut hint ----------
shortcut_label = Label(
    window,
    text="⏎ Press Enter to translate",
    font=("Helvetica", 9, "italic"),
    bg=COLORS["bg"],
    fg=COLORS["text_secondary"],
)
shortcut_label.place(x=30, y=215, anchor="w")

# ========== BOTTOM SECTION - OUTPUT ==========
# ---------- Separator ----------
separator = Frame(window, height=2, bg=COLORS["bg_secondary"])
separator.place(x=30, y=245, width=740)

# ---------- Output Title ----------
output_label_title = Label(
    window,
    text="📖 Translation Result",
    font=("Helvetica", 11, "bold"),
    bg=COLORS["bg"],
    fg=COLORS["text"],
)
output_label_title.place(x=30, y=280, anchor="w")

# ---------- Output Box (expanded) ----------
output_label = Label(
    window,
    text="✨ Your translation will appear here",
    height=7,
    bg=COLORS["entry_bg"],
    fg=COLORS["text_secondary"],
    font=("Helvetica", 13),
    width=54,
    justify="left",
    anchor="nw",
    relief="flat",
    padx=15,
    pady=12,
    wraplength=500,
)
output_label.place(x=30, y=310, anchor="w")

# ---------- Language indicators (visual feedback) ----------
source_indicator = Label(
    window,
    text="🇬🇧 Source: English",
    font=("Helvetica", 9),
    bg=COLORS["bg"],
    fg=COLORS["text_secondary"],
)
source_indicator.place(x=30, y=485, anchor="w")

target_indicator = Label(
    window,
    text="🇮🇷 Target: Persian",
    font=("Helvetica", 9),
    bg=COLORS["bg"],
    fg=COLORS["text_secondary"],
)
target_indicator.place(x=250, y=485, anchor="w")

# ---------- Update indicators when selection changes ----------
input_list.bind("<<ListboxSelect>>", update_indicators)
output_list.bind("<<ListboxSelect>>", update_indicators)

# ---------- Keyboard shortcut ----------
window.bind("<Return>", lambda event: enter())

# ---------- Footer ----------
footer = Label(
    window,
    text="💡 Tip: Select languages from the lists on the right • Click Translate or press Enter",
    font=("Helvetica", 8),
    bg=COLORS["bg"],
    fg=COLORS["text_secondary"],
)
footer.place(x=30, y=520, anchor="w")

# ---------- Run ----------
window.mainloop()
