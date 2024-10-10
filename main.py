import mesop as me

@me.page()
def app():
    me.text("Hello World")

wsgiapp = app

if __name__ == "__main__":
    from waitress import serve
    serve(wsgiapp, listen='127.0.0.1:5000')