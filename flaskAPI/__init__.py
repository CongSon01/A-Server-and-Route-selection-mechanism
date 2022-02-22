from api.app import RunFlask
def create_app():
    # instantiate the app
    app = RunFlask(__name__)

    #set up extensions
    return app

app = create_app()



    

   

   