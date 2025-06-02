from flask import Flask, request, render_template
from brevo_email import *
from dotenv import load_dotenv
import os
import pandas as pd
import joblib


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

file_path = r'Dataset\heart.csv'
data = pd.read_csv(file_path)
data = data.dropna()
numerical_features = list(data.select_dtypes(include=['float64', 'int64']).columns)
numerical_features.remove('HeartDisease')
numerical_features.remove('FastingBS')
print(numerical_features)

scaler = joblib.load(r'models\scaler.pkl')
rf_model = joblib.load(r'models\rf_model.pkl')
xgb_model = joblib.load(r'models\xgb_model.pkl')

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
        os.makedirs(upload_folder, exist_ok=True)  # Create folder if it doesn't exist
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


@app.route("/heart_predict", methods=["POST"])
def predict():
    data = {key: request.form[key] for key in request.form}
    print(data)
    age_average = 53
    restingbp_average = 132
    cholesterol_average = 199
    fastingBS_average = 0
    maxHR_average = 136
    
    age = data.get('age', age_average)
    if age == '':
        age = age_average
    gender = data.get('gender', 'M')
    if gender == '':
        gender = 'M'
    chest_pain = data.get('chestpain', "ASY")
    if chest_pain == '':
        chest_pain = 'ASY'
    restingbp = data.get('RestingBP', restingbp_average)
    if restingbp == '':
        restingbp = restingbp_average
    cholesterol = data.get('cholesterol_level', cholesterol_average)
    if cholesterol == '':
        cholesterol = cholesterol_average
    fastingBS = data.get('FastingBS', fastingBS_average)
    if fastingBS == '':
        fastingBS = fastingBS_average
    restingECG = data.get('RestingECG', "Normal")
    if restingECG == '':
        restingECG = 'Normal'
    maxHR = data.get('MaxHR', maxHR_average)
    if maxHR == '':
        maxHR = maxHR_average
    exerciseAngina = data.get('ExerciseAngina', 'N')
    if exerciseAngina == '':
        exerciseAngina = 'N'
    oldpeak = data.get('Oldpeak', 1)
    if oldpeak == '':
        oldpeak = 1
    st_slope = data.get('ST_Slope', 'Flat')
    if st_slope == '':
        st_slope = 'Flat'

    
    data_row = {
        'Age': age,
        'RestingBP': restingbp,
        'Cholesterol': cholesterol,
        'FastingBS': fastingBS,
        'MaxHR': maxHR,
        'Oldpeak': oldpeak,
        'ST_Slope': 2 if st_slope == "Up" else (1 if st_slope == "Flat" else 0),
        'Sex_M': 1 if gender == 'M' else 0,
        'ChestPainType_ATA': 1 if chest_pain == "ATA" else 0,
        'ChestPainType_NAP': 1 if chest_pain == "NAP" else 0,
        'ChestPainType_TA': 1 if chest_pain == "TA" else 0,
        'RestingECG_Normal': 1 if restingECG == "Normal" else 0,
        'RestingECG_ST': 1 if restingECG == "ST" else 0,
        'ExerciseAngina_Y': 1 if exerciseAngina == "Y" else 0
    }
    print("data row: ", data_row)
    print('before scalar transform')
    df_pred = pd.DataFrame([data_row])
    print(df_pred.head())
    rows_needed = scaler.get_feature_names_out()
    df_to_transform = df_pred[rows_needed]
    print(df_to_transform.head())
    row_pred = scaler.transform(df_to_transform)
    df_transformed = pd.DataFrame(row_pred, columns=df_to_transform.columns)

    # Add back missing columns from df_pred
    for col in df_pred.columns:
        if col not in df_transformed.columns:
            df_transformed[col] = df_pred[col].values  # Restore excluded columns


    def ensemble_classifier(t):
        counter_0 = 0
        counter_1 = 0
        y_pred_xg = xgb_model.predict(t)
        if y_pred_xg == [0]:
            counter_0 += 1
        else: 
            counter_1 += 1
        y_pred_rf = rf_model.predict(t)
        if y_pred_rf == [0]:
            counter_0 += 1
        else: 
            counter_1 += 1
        
        if counter_0 > counter_1:
            return 0
        else:
            return 1
        
    
    majority_pred = ensemble_classifier(df_transformed)

    output = ""
    if (majority_pred == 1):
        output += "You may have a heart problem, please go for a health checkup and consult a doctor.<br><br>"
        output += "Disclaimer: This is just a prediction from inputted data, any missing data can affect the accuracy significantly."
        output += "<br>Missing data is assigned by average or most frequent data"
    else:
        output += "No problems detected"

    return render_template('heart_predictor.html', output=output)

@app.route("/heart_predict", methods=["GET"])
def show_template():
    return render_template("heart_predictor.html")


if __name__ == '__main__':
    app.run()