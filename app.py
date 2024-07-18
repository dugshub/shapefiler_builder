from flask import render_template
import config
import models
import build_database


app = config.connex_app
app.add_api(config.basedir / 'swagger.yaml')


@app.route('/')
def home():  # put application's code here
    return render_template("home.html")


if __name__ == '__main__':
    build_database.build_db()
    app.run(host="0.0.0.0", port=8765,)



