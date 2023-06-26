from app import app
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.run(host='0.0.0.0',debug=True)
app.run(debug=True)