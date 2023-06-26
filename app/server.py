from flask import render_template, redirect, request, send_file, Response
from app.data_base_functions import *
from app.config_controll import read_config
from flask_socketio import SocketIO, emit
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from app import app



@app.route('/', methods=['GET'])
def main():
    print(f"Client get page from IP address: {request.remote_addr}")
    # config = read_config()
    # for i in get_column_names():
    #     print(config[i]["replacer_default_data"])
    return render_template("index.html", colums=get_column_names(), export_dlc=(len(get_column_names()) % 2 != 1), data=get_all_rows(), config=read_config(),zip=zip)


@app.route('/download', methods=['GET'])
def download():
    base_folder = Path(__file__).resolve().parent.parent / "data"
    filename = base_folder / "general_base.db"
    return send_file(filename, as_attachment=True)


socketio = SocketIO(app)


@socketio.on('connect')
def handle_connect():
    print(f"Client connected from IP address: {request.remote_addr}")


@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected from IP address: {request.remote_addr}")


@socketio.on('backup')
def handle():
    td = datetime.now()
    string = f'{td.strftime("%y-%m-%d")};{td.strftime("%H_%M_%f")[:-4]}.zip'
    base_folder = Path(__file__).resolve().parent.parent / "data"
    backups_folder = base_folder / "backups"
    zip_file_path = backups_folder / string
    database_path = base_folder / "general_base.db"
    with ZipFile(zip_file_path, "w") as myzip:
        myzip.write(database_path, arcname=database_path.name)
    print("backup")
    socketio.emit('notification', ("успешно",
                  "резервная копия ДБ создана!"))

@socketio.on('update')
def handle_message(data):
    update = 0
    for i in data:
        if i != {}:
            if i['id'][-1] == "D":
                print(delete_row_by_id(int(i['id'][:-1])))
            else:
                updated_data = ([value for key, value in i.items() if key != 'id'])
                if update_row(int(i['id']), updated_data) == True:
                    update += 1
    print(f"updated:{update}")
    socketio.emit('notification', (f"успешно x{update}", "сохранено"))

@socketio.on('export')
def handle_message(data):
    if data[1] != []:
        divider = data[0]
        exportData = []
        if data[3]:
            string = ""
            for i in data[1]:
                exportData.append(i)
            exportData = [f"{divider}".join(exportData)]
        if data[2] == "":
            for i in get_column_data(",".join(data[1])):
                string = ""
                for j in i:
                    string += str(j) + divider
                exportData.append(string[:-1])
        else:
            x = 1
            for i in get_column_data(",".join(data[1])):
                if data[2] == "" or int(data[2]) >= x:
                    x += 1
                else:
                    break
                string = ""
                for j in i:
                    string += str(j) + divider
                exportData.append(string[:-1])
    else:
        exportData = ["error"]
    socketio.emit('export', exportData)

@socketio.on('import')
def handle_message(data):
    errors = []
    sucress = 0
    for i in [item.split(data[0]) for item in data[2].split("\n")]:
        tryis = add_row(i,data[1])
        if tryis == True:
            sucress += 1
        else:
            errors.append([tryis,i])
    if errors != []:
        print(f"названия столбцов:{data[1]}")
        for error in errors:
            print(f"ошибка в строке: {error[1]},\nлог ошибки: {error[0]}")
        socketio.emit('notification', (f"ошибка x{len(errors)}", f"успешно x{sucress}\n подробнее в логах"))
    else:
        socketio.emit('notification', (f"успешно x{sucress}", "данные импортированны,\nобновите страницу для их отображения"))