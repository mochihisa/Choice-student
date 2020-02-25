import locale
import eel
import random
import pickle
import os
import sys
import datetime
from tkinter import filedialog, Tk
import platform
import copy


def main():
    eel.init("web")
    eel.start("main.html")


Student_names = []
Student_FILENAME = "./data/list.txt"
Student_FILENAME_raw = "./data/list_raw.txt"

# Student
@eel.expose
def Student_load():
    with open(select_file(), "r") as f:
        global Student_names
        Student_names = f.read().splitlines()
        Student_save(Student_FILENAME)
        Student_save(Student_FILENAME_raw)


@eel.expose
def Student_reset():
    Student_names_load(Student_FILENAME_raw)


@eel.expose
def Student_show():
    Student_names_load(Student_FILENAME)
    name_ls = ""
    a = 1
    for name in Student_names:
        if a % 5 == 0:
            name_ls = name_ls + name + "<br>"
        else:
            name_ls = name_ls + name + "　"
        a += 1
    return name_ls


@eel.expose
def Student_choice():
    Student_names_load(Student_FILENAME)
    global Student_names_raw
    Student_names_raw = copy.deepcopy(Student_names)
    if not Student_names:
        return
    global name
    name = random.choice(Student_names)
    Student_names.remove(name)
    if Student_names == []:
        Student_names_load(Student_FILENAME_raw)
    History_add(name)
    Student_save(Student_FILENAME)
    return name


@eel.expose
def Student_save(FILENAME):
    f = open(FILENAME, 'wb')
    pickle.dump(Student_names, f)


@eel.expose
def Student_names_load(FILENAME):
    f = open(FILENAME, "rb")
    global Student_names
    Student_names = pickle.load(f)


# History
History_FILENAME = "./data/history.txt"
History_data = []


@eel.expose
def History_load():
    with open(History_FILENAME, "r") as f:
        global History_data
        History_data = f.read().splitlines()


@eel.expose
def History_save():
    with open(History_FILENAME, "w") as f:
        for history in History_data:
            print(history, file=f)


@eel.expose
def History_show():
    history_ls = ""
    History_load()
    for history in History_data:
        history_ls = history + "<br>" + history_ls
    return history_ls


locale.setlocale(locale.LC_ALL, '')
@eel.expose
def History_add(name):
    now = datetime.datetime.now()
    History_data.append(f"{now:%m月%d日}:{name}")
    History_save()


@eel.expose
def History_cancel():
    History_data.pop()
    History_save()
    global Student_names
    Student_names = copy.deepcopy(Student_names_raw)
    Student_save(Student_FILENAME)


@eel.expose
def History_clear():
    global History_data
    History_data = []
    History_save()


# 名簿読み込み
# ダイアログ用のルートウィンドウの作成
# （root自体はeelのウィンドウとは関係ないので非表示にしておくのが望ましい）
root = Tk()
# ウィンドウサイズを0にする
root.geometry("0x0")
# ウィンドウのタイトルバーを消す
root.overrideredirect(1)
# ウィンドウを非表示に
root.withdraw()
system = platform.system()


@eel.expose
def select_file():
    # Windowsの場合withdrawの状態だとダイアログも
    # 非表示になるため、rootウィンドウを表示する
    if system == "Windows":
        root.deiconify()
    # macOS用にダイアログ作成前後でupdate()を呼ぶ
    root.update()

    # ダイアログを前面に
    # topmost指定(最前面)
    root.attributes('-topmost', True)
    root.withdraw()
    root.lift()
    root.focus_force()
    path_str = filedialog.askopenfilename()
    root.update()
    if system == "Windows":
        # 再度非表示化（Windowsのみ）
        root.withdraw()
    #path = Path(path_str)
    return path_str


if __name__ == '__main__':
    main()
