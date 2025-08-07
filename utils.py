from datetime import datetime

def format_data(remedios_db, diarios_db):
    remedios = []
    diarios = []

    if remedios_db:
        for r in remedios_db:
            id, data, tomou = r
            if data:
                try:
                    data_obj = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    data_obj = datetime.strptime(data, "%Y-%m-%d")
                new_data = data_obj.strftime('%d/%m/%Y')
            else:
                new_data = ""
            remedios.append({"id": id, "data": new_data, "tomou": tomou})

    if diarios_db:
        for d in diarios_db:
            id, data, texto = d
            if data:
                try:
                    data_obj = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    data_obj = datetime.strptime(data, "%Y-%m-%d")
                new_data = data_obj.strftime('%d/%m/%Y')
            else:
                new_data = ""
            diarios.append({"id": id, "data": new_data, "texto": texto})

    return remedios, diarios
