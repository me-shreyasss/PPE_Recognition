import os
from flask import Flask, render_template, request, jsonify
from roboflow import Roboflow
    
app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/shrey/Desktop/ppe_rec'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def run_script(file_path):
    # visualize your prediction
    rf = Roboflow(api_key="jXhXZWSys4F1FogpsNi6")
    project = rf.workspace().project("ppe-wlllw-n9oz8")
    model = project.version(1).model
    model.predict(file_path, confidence=50, overlap=30).save("prediction.jpg")
    
    return "Python script has been executed!"

@app.route('/')
def index():
    return render_template('web2.html')

@app.route('/run-script', methods=['GET', 'POST'])
def run_script_route():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        # If no file was selected
        if file.filename == '':
            return 'No selected file'
        
        # If a file is selected, save it to the defined folder
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
        
    result = run_script(file_path)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)