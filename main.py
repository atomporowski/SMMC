from mainwebsite import make_app

app = make_app()
if __name__ == '__main__':
    app.run(debug=True, port=5050, host="0.0.0.0")
