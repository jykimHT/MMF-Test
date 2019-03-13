from tkinter import *
import tkinter.ttk
import mmf_test


class TestTool:
    # Drawing window
    def __init__(self, window):
        # main window
        self.window = window
        self.window.title("MMF Test ver.1.0.2")
        self.window.geometry("1100x630+200+200")    # width x height + initialX + initialY
        self.window.resizable(False, False)

        # Label
        Label(self.window, text="IP").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        Label(self.window, text="").grid(row=0, column=2, padx=20)
        Label(self.window, text="Port").grid(row=0, column=3, padx=10, pady=10, sticky="e")
        Label(self.window, text="ID").grid(row=1, column=0, padx=10, pady=4, sticky="e")
        Label(self.window, text="PW").grid(row=2, column=0, padx=10, pady=2, sticky="e")
        Label(self.window, text="UUID\n(Optional)", justify="right").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        Label(self.window, text="type").grid(row=1, column=3, padx=10, pady=4, sticky="e")
        Label(self.window, text="subType").grid(row=2, column=3, padx=10, pady=2, sticky="e")
        Label(self.window, text="Request").grid(row=4, column=0, padx=10, pady=10, sticky="nw")
        Label(self.window, text="MMF Type").grid(row=3, column=3, padx=10, pady=2, sticky="e")
        Label(self.window, text="Response").grid(row=4, column=3, padx=10, pady=10, sticky="nw")

        # Entry
        self.text_ip = Entry(self.window, textvariable=StringVar(self.window, value='127.0.0.1'), width=20)
        self.text_port = Entry(self.window, textvariable=StringVar(self.window, value='25301'), width=10)
        self.text_id = Entry(self.window, width=20)
        self.text_pw = Entry(self.window, width=20)
        self.text_uuid = Entry(self.window, width=30)
        self.text_type = Entry(self.window, width=10)
        self.text_sub_type = Entry(self.window, width=10)

        self.text_ip.grid(row=0, column=1,sticky="w")
        self.text_port.grid(row=0, column=4, sticky="w")
        self.text_id.grid(row=1, column=1, sticky="w")
        self.text_pw.grid(row=2, column=1, sticky="w")
        self.text_uuid.grid(row=3, column=1, sticky="w")
        self.text_type.grid(row=1, column=4, sticky="w")
        self.text_sub_type.grid(row=2, column=4, sticky="w")

        # Combobox
        mmf_type_list = ["이마주", "대림"]
        self.combo_mmf_type = tkinter.ttk.Combobox(self.window, values=mmf_type_list, state='readonly')
        self.combo_mmf_type.grid(row=3, column=4, sticky="w")
        self.combo_mmf_type.set("이마주")

        # Text & Scrollbar
        self.text_req = Text(self.window, height=30, width=55, wrap=CHAR)
        self.text_req.grid(row=4, column=1, sticky="e")
        self.req_y_scroll = Scrollbar(self.window, command=self.text_req.yview)
        self.text_req.config(yscrollcommand=self.req_y_scroll.set)
        self.req_y_scroll.grid(row=4, column=2, sticky='nsw')

        self.text_res = Text(self.window, height=30, width=65, wrap=CHAR)
        self.text_res.grid(row=4, column=4, sticky="e")
        self.res_y_scroll = Scrollbar(self.window, command=self.text_res.yview)
        self.text_res.config(yscrollcommand=self.res_y_scroll.set)
        self.res_y_scroll.grid(row=4, column=5, sticky='nsw')

        # Button
        Button(self.window, text="전송", height=2, width=10, command=self.send_request).grid(row=5, column=4, padx=10, pady=15, sticky="e")

        mainloop()

    def send_request(self):

        mmf_type = self.combo_mmf_type.get()
        ip = self.text_ip.get()
        port = int(self.text_port.get())

        id = self.text_id.get()
        pw = self.text_pw.get()
        uuid = self.text_uuid.get()

        type = int(self.text_type.get())
        sub = int(self.text_sub_type.get())
        body = self.text_req.get("1.0", END)

        req_info = mmf_test.RequestInfo(mmf_type, ip, port, id, pw, uuid, type, sub, body)
        response = mmf_test.send_message(req_info)
        self.text_res.delete("1.0", END)
        self.text_res.insert("1.0", response)


window = Tk()
test_tool = TestTool(window)
