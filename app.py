
from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta

app = Flask(__name__)

# Sample medicine inventory
medicines = [
    {
        "id": 1,
        "name": "Paracetamol",
        "batch": "B101",
        "quantity": 100,
        "expiry": date.today() - timedelta(days=10)
    },
    {
        "id": 2,
        "name": "Cough Syrup",
        "batch": "B102",
        "quantity": 50,
        "expiry": date.today() + timedelta(days=10)
    },
    {
        "id": 3,
        "name": "Vitamin C",
        "batch": "B103",
        "quantity": 80,
        "expiry": date.today() + timedelta(days=200)
    },
    {
        "id": 4,
        "name": "Amoxicillin",
        "batch": "B104",
        "quantity": 40,
        "expiry": date.today() + timedelta(days=5)
    },
    {
        "id": 5,
        "name": "Cetirizine",
        "batch": "B105",
        "quantity": 60,
        "expiry": date.today() + timedelta(days=120)
    },
    {
        "id": 6,
        "name": "Ibuprofen",
        "batch": "B106",
        "quantity": 30,
        "expiry": date.today() - timedelta(days=3)
    }
]


# Determine medicine expiry status
def get_status(medicine):
    days_left = (medicine["expiry"] - date.today()).days

    if days_left < 0:
        return "Expired"
    elif days_left <= 30:
        return "Expiring Soon"
    else:
        return "Safe"


# Dashboard page
@app.route("/")
def home():
    total = len(medicines)

    expired = sum(
        1 for medicine in medicines
        if get_status(medicine) == "Expired"
    )

    soon = sum(
        1 for medicine in medicines
        if get_status(medicine) == "Expiring Soon"
    )

    safe = total - expired - soon

    return render_template(
        "index.html",
        total=total,
        expired=expired,
        soon=soon,
        safe=safe,
        medicines=medicines,
        get_status=get_status
    )


# Medicine inventory page
@app.route("/medicines")
def medicine_list():
    search = request.args.get("search", "").strip().lower()
    status_filter = request.args.get("status", "").strip()

    filtered_medicines = medicines

    if search:
        filtered_medicines = [
            medicine for medicine in filtered_medicines
            if search in medicine["name"].lower()
            or search in medicine["batch"].lower()
        ]

    if status_filter in ("Safe", "Expiring Soon", "Expired"):
        filtered_medicines = [
            medicine for medicine in filtered_medicines
            if get_status(medicine) == status_filter
        ]

    return render_template(
        "medicines.html",
        medicines=filtered_medicines,
        get_status=get_status
    )


# Expiry alerts page
@app.route("/alerts")
def alerts():
    alert_medicines = [
        medicine for medicine in medicines
        if get_status(medicine) in ("Expired", "Expiring Soon")
    ]

    # Show expired medicines first
    alert_medicines.sort(
        key=lambda medicine: medicine["expiry"]
    )

    return render_template(
        "alerts.html",
        medicines=alert_medicines,
        get_status=get_status
    )


# Add a new medicine
@app.route("/add", methods=["POST"])
def add_medicine():
    name = request.form.get("name", "").strip()
    batch = request.form.get("batch", "").strip()
    quantity_text = request.form.get("quantity", "").strip()
    expiry_text = request.form.get("expiry", "").strip()

    if not name or not batch or not quantity_text or not expiry_text:
        return "Please fill in all medicine details.", 400

    try:
        quantity = int(quantity_text)
        expiry_date = date.fromisoformat(expiry_text)

        if quantity <= 0:
            return "Quantity must be greater than zero.", 400

    except ValueError:
        return "Enter a valid quantity and expiry date.", 400

    medicines.append({
        "id": max(
            (medicine["id"] for medicine in medicines),
            default=0
        ) + 1,
        "name": name,
        "batch": batch,
        "quantity": quantity,
        "expiry": expiry_date
    })

    return redirect(url_for("medicine_list"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
