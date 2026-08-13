from tkinter import *
from translation_base import *


def enter():

    input_text = input_entry.get()

    if not input_text:
        output_lable.config(fg="red", text="Dont put Entry box empty")
        return

    # ---------- source ----------
    selected_input = input_list.curselection()

    if selected_input:
        source = symbol[selected_input[0]]
    else:
        source = "en"

    # ---------- target ----------
    selected_output = output_list.curselection()

    if selected_output:
        target = symbol[selected_output[0]]
    else:
        target = "fa"

    data = create_data(src=source, tgt=target, txt=input_text)
    url, header = url_header()
    response = sending_request(data, url=url, header=header)
    if not response:
        output_lable.config(fg="red", text="Error please try again")
    else:
        output_lable.config(fg="black", text=response)
    return


languages = [
    "persian",
    "english",
    "spanish",
    "arabic",
    "japanese",
    "russian",
    "chinese",
    "german",
    "italic",
]

symbol = [
    "fa",
    "en",
    "es",
    "ar",
    "ja",
    "ru",
    "zh",
    "de",
    "it",
]
window = Tk()
# -----------window--------------
window.title("Kamyar Translator")
window.geometry("600x400")
window.configure(bg="#269ADE")
window.resizable(False, False)

# -----------input Entry--------------
input_entry = Entry(
    window,
    width=40,
    font=("Arial", 14, "bold"),
    background="white",
    justify="left",
)
input_entry.place(x=30, y=50, anchor="w")

# -----------input list box--------------
input_list = Listbox(
    window,
    width=10,
    height=5,
    bg="white",
    fg="black",
    activestyle="dotbox",
    exportselection=False,
)
i = 0
for name in languages:

    input_list.insert(END, name)
    if i % 2 == 0:
        input_list.itemconfig(i, bg="white")
    else:
        input_list.itemconfig(i, bg="#EDEBEA")
    i += 1

input_list.place(x=500, y=80, anchor="w")

# -------------OutPut lable-------------
output_lable = Label(
    window,
    text="this is the test text\nline 2",
    height=5,
    bg="white",
    font=("Arial", 14, "bold"),
    width=36,
    justify="left",  # *
    anchor="nw",  # *
)
output_lable.place(x=30, y=250, anchor="w")

# -----------output list box--------------
output_list = Listbox(
    window,
    width=10,
    height=5,
    bg="white",
    fg="black",
    activestyle="dotbox",
    exportselection=False,
)
i = 0
for name in languages:

    output_list.insert(END, name)
    if i % 2 == 0:
        output_list.itemconfig(i, bg="white")
    else:
        output_list.itemconfig(i, bg="#EDEBEA")
    i += 1

output_list.place(x=500, y=250, anchor="w")

# ------------submit button----------
submit_button = Button(
    window,
    bg="#F46608",
    fg="white",
    text="translate",
    activebackground="#269ADE",
    activeforeground="white",
    font=("Arial", 17, "italic"),
    width="10",
    command=enter,
)
submit_button.place(x=30, y=130, anchor="w")
window.mainloop()
