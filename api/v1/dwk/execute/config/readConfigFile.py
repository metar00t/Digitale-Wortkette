import configparser
def read_db_params():
    # liest die Umgebungsvariablen
    config = configparser.ConfigParser()
    config.read('config/.config')
    return config