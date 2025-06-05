from flask import Flask, request, render_template
from brevo_email import *
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()
my_name = os.getenv('MY_NAME')
job_title = os.getenv('JOB_TITLE')
contact_email = os.getenv('CONTACT_EMAIL')
phone_no = os.getenv('PHONE_NO')
linkedin = os.getenv('LINKEDIN')
github = os.getenv('GITHUB')
if github == "" or "None":
    github = None


# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
sender = os.getenv('BREVO_DOMAIN_EMAIL')
name = os.getenv('BREVO_SENDER_NAME')
print(configuration.api_key['api-key'])
print(sender)
print(name)

rag_folder_path = os.path.join(app.static_folder, 'images', 'rag')

rag_images = [
    os.path.join('images', 'rag', filename).replace('\\', '/')
    for filename in os.listdir(rag_folder_path)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
]

landslide_folder_path = os.path.join(app.static_folder, 'images', 'landslide')

landslide_images = [
    os.path.join('images', 'landslide', filename).replace('\\', '/')
    for filename in os.listdir(landslide_folder_path)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
]

@app.route('/')
def home():
    print(rag_images)
    print(landslide_images)
    return render_template('index.html', name=my_name, job_title=job_title,
                           contact_email=contact_email, phone_no=phone_no, 
                           linkedin=linkedin, github=github, rag_images=rag_images,
                           landslide_images=landslide_images)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Get the form data
    sender_email = request.form.get('email')
    context = request.form.get('context')
    file = request.files.get('file')  # Get the uploaded file

    if file:
        # Save the uploaded file to a directory (e.g., "uploads/")
        upload_folder = 'temp_upload'
        file_name = file.filename
        print('filename: ', file_name)
        file_path = os.path.join(upload_folder, file_name)
        file.save(file_path)
        print(f"File saved at: {file_path}")
        with open(file_path, 'rb') as file:
            file_data = file.read()

            subject_automated = "Portofolio Contact " + str(datetime.datetime.now())
            html_automated = f"Sent By: {sender_email} \n\n" + context
            encoded_file = base64.b64encode(file_data).decode('utf-8')

            brevo_send_attachment(to_email=contact_email, to_name=sender_email ,subject=subject_automated, 
               html_content=html_automated, attachment=encoded_file, attachment_name=file_name)
            print("email successfully sent")
        os.remove(file_path)
    else:
        print("Entered Else")
        subject_automated = "Portofolio Contact " + str(datetime.datetime.now())
        html_automated = f"Sent By: {sender_email} \n\n" + context
        brevo_send(to_email=contact_email, to_name=sender_email ,subject=subject_automated, 
               html_content=html_automated)
    
    # Add logic here to handle the form data, e.g., send an email or save to the database
    return render_template('index.html', name=my_name, job_title=job_title,
                           contact_email=contact_email, phone_no=phone_no, 
                           linkedin=linkedin, github=github, rag_images=rag_images,
                           landslide_images=landslide_images)

if __name__ == '__main__':
    app.run(debug=True)