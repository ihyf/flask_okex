# coding:utf-8
from create_app import app
from flask import render_template
import view


@app.route("/123")
def test():
    return render_template("index.html")


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=1000)
    app.run(host="127.0.0.1", port=8888)

