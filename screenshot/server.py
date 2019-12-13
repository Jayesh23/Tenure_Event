from flask import Flask, send_from_directory, send_file
import pyscreenshot as ImageGrab
from datetime import datetime

app = Flask(__name__) 
  
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function. 
@app.route('/') 
# ‘/’ URL is bound with hello_world() function. 
def hello_world(): 
    im = ImageGrab.grab()
    name = 'screenshot'+str(datetime.now())+'.png'
    im.save(name)
    return send_file(name, attachment_filename=name)


    # response = send_from_directory(director='', filename='screenshot'+str(datetime.now())+'.png')
    # response.headers['my-custom-header'] = 'my-custom-status-0'
    # return response

    # return im
    # return "success"

# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(host="0.0.0.0", port="8080") 