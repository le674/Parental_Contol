from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def get_time():
    print('Incoming..')
    print(str(request.get_json()))
    return 'OK',200


@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')

if __name__ =='__main__':
    app.run(debug = True)
