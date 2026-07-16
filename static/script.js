let reportData = {};
async function predictHeart() {

    const form = document.getElementById("heartForm");

    if (!form.age.value || !form.thalach.value || !form.oldpeak.value || !form.trestbps.value) {
        alert("Please fill in all required fields before predicting.");
        return;
    }

    if (form.age.value < 1 || form.age.value > 150) {
        alert("Please enter correct Age!");
        return;
    }

    if (form.thalach.value <= 21 || form.thalach.value >= 221) {
        alert("Please enter correct Maximum Heart Rate!");
        return;
    }

    if (form.oldpeak.value < 0 || form.oldpeak.value >= 7) {
        alert("Please enter correct OldPeak value!");
        return;
    }

    if (form.trestbps.value <= 81 || form.trestbps.value >= 211) {
        alert("Please enter correct Resting Blood Pressure!");
        return;
    }

    const patientName = document.getElementById("patientName").value.trim();

    const data = {

        name: document.getElementById("patientName").value,
        phone: document.getElementById("phone").value,
        age: form.age.value,
        sex: form.sex.value,
        cp: form.cp.value,
        restecg: form.restecg.value,
        thalach: form.thalach.value,
        exang: form.exang.value,
        oldpeak: form.oldpeak.value,
        slope: form.slope.value,
        ca: form.ca.value,
        thal: form.thal.value,
        trestbps: form.trestbps.value
    };

    try {
        document.getElementById("result").style.display = "none";
        document.getElementById("loadingScreen").style.display = "flex";

        const loadingText = document.getElementById("loadingText");
        const loadingFill = document.getElementById("loadingFill");

        loadingFill.style.width = "0%";

        loadingText.innerHTML = "Initializing AI Model...";

        setTimeout(() => {
            loadingFill.style.width = "25%";
            loadingText.innerHTML = "Checking Patient Information...";
        }, 500);

        setTimeout(() => {
            loadingFill.style.width = "50%";
            loadingText.innerHTML = "Analyzing Heart Parameters...";
        }, 1200);

        setTimeout(() => {
            loadingFill.style.width = "75%";
            loadingText.innerHTML = "Running Neural Network...";
        }, 1900);

        setTimeout(() => {
            loadingFill.style.width = "100%";
            loadingText.innerHTML = "Generating Prediction...";
        }, 2500);
        await new Promise(resolve => setTimeout(resolve, 3000));

        document.getElementById("loadingScreen").style.display = "none";

        document.getElementById("result").style.display = "block";
        document.getElementById("result").innerHTML = `
        <div class="result-card loading">
            <h2>🩺 Analyzing Patient Data...</h2>
        </div>
        `;

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!result.success) {

            document.getElementById("result").innerHTML = `
            <div class="result-card high">
                <h2>❌ Error</h2>
                <p>${result.error}</p>
            </div>
            `;

            return;
        }

        const risk = Number((100 - result.probability).toFixed(1));

        let title = "";
        let icon = "";
        let color = "";
        let advice = "";

        if (risk >= 90) {

            title = "Extremely High Risk";
            icon = "🚨";
            color = "#ff1744";

            advice =
                "Immediate medical consultation is highly recommended.";

        }

        else if (risk >= 50) {

            title = "High Risk";
            icon = "⚠️";
            color = "#ff9800";

            advice =
                "Please consult a cardiologist as soon as possible.";

        }

        else if (risk >= 15) {

            title = "Moderate Risk";
            icon = "🟡";
            color = "#ffd600";

            advice =
                "Maintain a healthy lifestyle and undergo routine checkups.";

        }

        else {

            title = "Low Risk";
            icon = "✅";
            color = "#00e676";

            advice =
                "Maintain regular exercise, a healthy diet and yearly checkups.";

        }

        document.getElementById("result").innerHTML = `

        <div class="result-card">

            <h2>${icon} ${title}</h2>

            <div class="meter-header">

                <span>Risk Probability</span>

                <span>${risk}%</span>

            </div>

            <div class="meter">

                <div
                    class="meter-fill"
                    style="
                        width:${risk}%;
                        background:${color};
                    ">
                </div>

            </div>

            <div class="score">

                ${risk}%

            </div>

            <div class="recommendation">

                <h3>💡 Recommendation</h3>

                <p>${advice}</p>

            </div>

        </div>

        `;
        let cpNames = {
            0: "Typical Angina",
            1: "Atypical Angina",
            2: "Non-anginal Pain",
            3: "Asymptomatic"
        };
        let slopeNames = {
            0: "Upsloping",
            1: "Flat",
            2: "Downsloping"
        };
        let thalNames = {
            1: "unknown",
            2: "Normal",
            3: "Fixed Defect",
            4: "Reversable Defect"
        };
        let restecgNames = {
            0: "Normal",
            1: "ST-T Wave Abnormality",
            2: "Left Ventricular Hypertrophy"
        };
        let exangNames = {
            0: "No",
            1: "Yes"
        };
        reportData = {

            name: data.name,
            phone: data.phone,
            age: data.age,
            gender: data.sex == 1 ? "Male" : "Female",
            heartRate: data.thalach,
            bp: data.trestbps,
            cp: cpNames[data.cp],
            oldpeak: data.oldpeak,
            slope: slopeNames[data.slope],
            ca: data.ca,
            thal: thalNames[data.thal],
            restecg: restecgNames[data.restecg],
            exang: exangNames[data.exang],
            probability: risk,
            prediction: title,
            recommendation: advice

        }
        document.getElementById("downloadBtn").style.display = "block";

    }

    catch (error) {

        document.getElementById("result").innerHTML = `
        <div class="result-card high">
            <h2>Server Error</h2>
            <p>${error}</p>
        </div>
        `;
        let cpNames = {
            0: "Typical Angina",
            1: "Atypical Angina",
            2: "Non-anginal Pain",
            3: "Asymptomatic"
        };
        reportData = {
            name: data.name,
            age: data.age,
            gender: data.sex == 1 ? "Male" : "Female",
            heartRate: data.thalach,
            bp: data.trestbps,
            cp: cpNames[data.cp],
            slope: data.slope,
            ca: data.ca,
            thal: data.thal,
            restecg: data.restecg,
            exang: data.exang,
            oldpeak: data.oldpeak,
            probability: risk,
            prediction: title,
            recommendation: advice

        }
    }




}
async function downloadReport() {

    const response = await fetch("/download_report", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(reportData)

    });

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "Heart_Report.pdf";

    a.click();

}
