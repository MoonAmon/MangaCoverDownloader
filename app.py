from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def set_manga_folder():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
