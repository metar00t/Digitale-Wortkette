from flask import Flask, render_template

app = Flask(__name__)

# Hier wird der Main Code stehen, der ausgeführt wird
@app.route("/api/v1/dwk/home")
def start():
    return render_template("landingpage.html")

if __name__ == '__main__':
    app.run(debug = True)