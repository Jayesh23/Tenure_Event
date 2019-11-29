from flask import Flask 
import pyscreenshot as ImageGrab

app = Flask(__name__) 
  
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function. 
@app.route('/') 
# ‘/’ URL is bound with hello_world() function. 
def hello_world(): 
    im = ImageGrab.grab()
    im.save('screenshot.png')
    # im.show()
    return "success"

# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(host="0.0.0.0", port="8080") 