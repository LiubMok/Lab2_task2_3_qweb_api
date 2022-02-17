from flask import Flask, render_template, request
import functionality

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('index.html')


@app.route('/')
def dashboard_errors(h_file):
    return render_template(h_file)


@app.route('/create/map', methods=['GET', 'POST'])
def create():
    name = request.form.get('domain')
    number_of_friends = request.form.get('amount')
    try:
        int(number_of_friends)
        return functionality.main(name, number_of_friends)
    except ValueError:
        return dashboard_errors('for_errors.html')


if __name__ == "__main__":
    app.run(debug=True)
