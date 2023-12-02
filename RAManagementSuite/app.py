from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.debug = True
    # app.run(host='0.0.0.0', port=8080)   # Use this entry when use docker, open 127.0.0.1:8080 on your browser
    app.run()
