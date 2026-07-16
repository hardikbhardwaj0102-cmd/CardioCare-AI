from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import joblib
import io
from datetime import datetime

from tensorflow.keras.models import load_model

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

app = Flask(__name__)

# ============================================================
# PROFESSIONAL PDF REPORT
# ============================================================

@app.route("/download_report", methods=["POST"])
def download_report():
    data = request.get_json()
    print("PDF DATA:", data)
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.darkred

    body_style = styles["BodyText"]

    elements = []

    # ========================================================
    # HEADER
    # ========================================================

    elements.append(
        Paragraph(
            "<font color='#C62828'><b>   CardioCare AI</b></font>",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "<b>AI Heart Disease Prediction Report</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1,10))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=colors.darkred
        )
    )

    elements.append(Spacer(1,18))

    # ========================================================
    # PATIENT INFORMATION
    # ========================================================

    elements.append(
        Paragraph("<b>Patient Information</b>", heading_style)
    )

    elements.append(HRFlowable(width="100%"))

    elements.append(Spacer(1,10))

    patient_table = [
    ["Patient Name", data.get("name", "N/A")],
    ["Mobile Number", data.get("phone", "N/A")],
    ["Age", f"{data['age']} Years"],
    ["Gender", data["gender"]],
    ["Heart Rate", f"{data['heartRate']} bpm"],
    ["Blood Pressure", f"{data['bp']} mmHg"],
    ["Chest Pain", data.get("cp", "N/A")],
    ["Old Peak", data["oldpeak"]],
    ["Slope", data.get("slope", "N/A")],
    ["Number of Major Vessels", data.get("ca", "N/A")],
    ["Thalassemia", data.get("thal", "N/A")],
    ["Resting ECG", data.get("restecg", "N/A")],
    ["Exercise Induced Angina", data.get("exang", "N/A")]
]   

    table = Table(patient_table, colWidths=[170,250])

    table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BACKGROUND",(0,0),(0,-1),colors.whitesmoke),

        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("TOPPADDING",(0,0),(-1,-1),8)

    ]))

    elements.append(table)

    elements.append(Spacer(1,20))

    # ========================================================
    # PREDICTION
    # ========================================================

    elements.append(
        Paragraph("<b>Prediction</b>", heading_style)
    )

    elements.append(HRFlowable(width="100%"))

    elements.append(Spacer(1,10))

    prediction_table = Table(

        [

            [f"{data['prediction'].upper()}"],

            [f"Risk Probability : {data['probability']}%"]

        ],

        colWidths=[420]

    )
    
    prediction_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#C62828")),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("BACKGROUND",(0,1),(-1,1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

        ("FONTSIZE",(0,0),(-1,0),16),

        ("BOTTOMPADDING",(0,0),(-1,-1),12),

        ("TOPPADDING",(0,0),(-1,-1),12),

        ("GRID",(0,0),(-1,-1),1,colors.grey)

    ]))

    elements.append(prediction_table)

    elements.append(Spacer(1,20))

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    elements.append(
        Paragraph("<b>Recommendations</b>", heading_style)
    )

    elements.append(HRFlowable(width="100%"))

    elements.append(Spacer(1,10))

    recommendations = [

        "✓ Consult a cardiologist.",

        "✓ Exercise at least 30 minutes daily.",

        "✓ Maintain a healthy balanced diet.",

        "✓ Reduce salt and saturated fat intake.",

        "✓ Monitor blood pressure regularly."

    ]

    for rec in recommendations:

        elements.append(
            Paragraph(rec, body_style)
        )

    elements.append(Spacer(1,20))
        # ========================================================
    # MODEL INFORMATION
    # ========================================================

    elements.append(
        Paragraph("<b>Model Information</b>", heading_style)
    )

    elements.append(
        HRFlowable(width="100%")
    )

    elements.append(Spacer(1,10))

    model_table = [

        ["Model","Artificial Neural Network (ANN)"],

        ["Framework","TensorFlow / Keras"],

        ["Features Used","11"],

        ["Accuracy","90.1%"],

        ["Prediction Time","< 0.02 sec"]

    ]

    model = Table(
        model_table,
        colWidths=[170,250]
    )

    model.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BACKGROUND",(0,0),(0,-1),colors.whitesmoke),

        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("TOPPADDING",(0,0),(-1,-1),8)

    ]))

    elements.append(model)

    elements.append(Spacer(1,20))

    # ========================================================
    # DISCLAIMER
    # ========================================================

    elements.append(
        Paragraph("<b>Disclaimer</b>", heading_style)
    )

    elements.append(
        HRFlowable(width="100%")
    )

    elements.append(Spacer(1,10))

    disclaimer = """
    This report has been generated using an Artificial Intelligence
    model for educational purposes only. It should not be used as a
    substitute for professional medical diagnosis or treatment.
    Please consult a qualified healthcare professional before making
    any medical decisions.
    """

    elements.append(
        Paragraph(disclaimer, body_style)
    )

    elements.append(Spacer(1,20))

    # ========================================================
    # FOOTER
    # ========================================================

    elements.append(
        HRFlowable(width="100%")
    )

    elements.append(Spacer(1,10))

    now = datetime.now()

    elements.append(
        Paragraph(
            f"<b>Generated On :</b> {now.strftime('%d %B %Y | %I:%M %p')}",
            body_style
        )
    )

    elements.append(
        Paragraph(
            "<font color='grey'>Generated by CardioCare AI</font>",
            body_style
        )
    )

    elements.append(
        Paragraph(
            "<font color='grey'>© 2026 CardioCare AI</font>",
            body_style
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Heart_Report.pdf",
        mimetype="application/pdf"
    )
# ============================================================
# LOAD MODEL
# ============================================================

model = load_model("heart_disease_ann.keras")
ct = joblib.load("transformer.pkl")


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("heart.html")


# ============================================================
# HEART DISEASE PREDICTION
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        age = int(data["age"])
        sex = int(data["sex"])
        cp = int(data["cp"])
        restecg = int(data["restecg"])
        thalach = int(data["thalach"])
        exang = int(data["exang"])
        oldpeak = float(data["oldpeak"])
        slope = int(data["slope"])
        ca = int(data["ca"])
        thal = int(data["thal"])
        trestbps = int(data["trestbps"])

        # Same preprocessing used while training

        trestbps_new = np.log1p(trestbps)

        df = pd.DataFrame({

            "age":[age],

            "thalach":[thalach],

            "trestbps_new":[trestbps_new],

            "sex":[sex],

            "cp":[cp],

            "restecg":[restecg],

            "exang":[exang],

            "oldpeak":[oldpeak],

            "slope":[slope],

            "ca":[ca],

            "thal":[thal]

        })

        # Apply Column Transformer

        transformed = ct.transform(df)

        # Neural Network Prediction

        pred = model.predict(
            transformed,
            verbose=0
        )

        probability = float(pred[0][0])

        prediction = 1 if probability >= 0.5 else 0

        probability = round(probability * 100, 2)
        return jsonify({

    "success": True,

    "prediction": prediction,

    "probability": probability,

    "age": age,
    "gender": "Male" if sex == 1 else "Female",
    "heartRate": thalach,
    "bp": trestbps,
    "cp": cp,
    "oldpeak": oldpeak,
    "slope": slope,
    "ca": ca,
    "thal": thal,
    "restecg": restecg,
    "exang": exang

})

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )