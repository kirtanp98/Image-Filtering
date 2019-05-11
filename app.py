from imageProc import app


if __name__ == '__main__':
    app.run(threaded = True, debug = True, port = 8080)
    #app.run(host ='192.168.1.150', port = 9000)
    print('App is running')