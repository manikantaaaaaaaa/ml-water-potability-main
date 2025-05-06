import os
import joblib
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Use only one level up
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


app = FastAPI()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/")
async def predict(request: Request, ph: float = Form(...), hardness: float = Form(...),
                solids: float = Form(...), chloramines: float = Form(...),
                sulfate: float = Form(...), conductivity: float = Form(...),
                organic_carbon: float = Form(...), trihalomethanes: float = Form(...),
                turbidity: float = Form(...)):

    message = "Based on the data that you wrote before, your water is: "
    data = [ph, hardness, solids, chloramines, sulfate, conductivity,
            organic_carbon, trihalomethanes, turbidity]

    # Check if all fields are zero
    if all(d == 0 for d in data):
        return templates.TemplateResponse("prediction.html", {
            "request": request,
            "alert_type": "alert-danger",
            "result": "Wait! 🤔 It seems like you filled all the data with zeros. Try again!",
            "img_url": "https://www.eucim.es/wp-content/uploads/2019/08/2378651-1500x1500-785x394.jpg",
            "title": "All data is zero"
        })

    # Load models
    scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.save"))
    model = joblib.load(os.path.join(BASE_DIR, "models", "svc.save"))

    # Normalize data
    norm_data = scaler.transform([data])

    # Get predictions
    prediction = model.predict(norm_data)

    # Values for templates
    positive_title = "The water is potable!"
    positive_img_url = "https://www.snf.co.uk/wp-content/uploads/2017/06/rsz_potabledrinkingwater.jpg"
    negative_title = "The water is not potable, careful!"
    negative_img_url = "https://cdn-reichelt.de/bilder/web/xxl_ws/C180/W-74105.png"

    # Set the variables based on prediction
    result = message + "POTABLE" if prediction[0] == 1 else message + "NOT POTABLE"
    img_url = positive_img_url if prediction[0] == 1 else negative_img_url
    alert_type = "alert-primary" if prediction[0] == 1 else "alert-danger"
    title = positive_title if prediction[0] == 1 else negative_title

    return templates.TemplateResponse("prediction.html", {
        "request": request,
        "alert_type": alert_type,
        "result": result,
        "img_url": img_url,
        "title": title
    })
