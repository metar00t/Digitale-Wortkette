import configparser
def read_db_params():
    # liest die Umgebungsvariablen
    config = configparser.ConfigParser()
    config.read('env/.env')
    return config