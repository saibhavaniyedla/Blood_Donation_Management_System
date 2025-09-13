import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import traceback

# ---------------- Helper: Send Email ----------------
def send_email(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = "saibhavaniyedla35@gmail.com"

    user = "saibhavaniyedla35@gmail.com"
    password = "rgcazacazvpapxqs"  # Gmail app password (no spaces)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")

# ---------------- Flask App ----------------
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# ---------------- Database Connection ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # 👈 replace with your MySQL password
    database="blood_donation"
)
cursor = db.cursor()

# ---------------- Donor Registration ----------------
@app.route('/donors', methods=['POST'])
def add_donor():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        age = data.get("age")
        blood_group = data.get("blood_group")
        phone = data.get("phone")
        location = data.get("location")

        sql = "INSERT INTO donors (name, email, age, blood_group, phone, location) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, email, age, blood_group, phone, location)
        cursor.execute(sql, values)
        db.commit()

        return jsonify({"message": "Donor registered successfully!"})
    except Exception as e:
        print("❌ Error in add_donor:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------- Blood Request ----------------
@app.route('/requests', methods=['POST'])
def add_request():
    try:
        data = request.json
        name = data.get("name")
        blood_group = data.get("blood_group")
        phone = data.get("phone")
        location = data.get("location")

        # Save request
        sql = "INSERT INTO requests (name, blood_group, phone, location) VALUES (%s, %s, %s, %s)"
        values = (name, blood_group, phone, location)
        cursor.execute(sql, values)
        db.commit()

        # Find matching donors
        cursor.execute("SELECT name, email FROM donors WHERE UPPER(blood_group) = %s", (blood_group.upper(),))
        donors = cursor.fetchall()

        # Send email notifications
        for donor in donors:
            donor_name, donor_email = donor
            subject = f"Urgent Blood Request for {blood_group}"
            body = f"""
            Dear {donor_name},

            A patient urgently needs {blood_group} blood.

            Patient: {name}
            Contact: {phone}
            Location: {location}

            Please consider donating if you are able.
            """
            send_email(subject, body, donor_email)

        return jsonify({"message": "Blood request submitted and donors notified!"})
    except Exception as e:
        print("❌ Error in add_request:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------- Get All Donors ----------------
@app.route('/donors', methods=['GET'])
def get_donors():
    try:
        cursor.execute("SELECT * FROM donors")
        result = cursor.fetchall()
        donors = []
        for row in result:
            donors.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3],
                "blood_group": row[4],
                "phone": row[5],
                "location": row[6],
                "last_donated": str(row[7]) if len(row) > 7 and row[7] else None
            })
        return jsonify(donors)
    except Exception as e:
        print("❌ Error in get_donors:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------- Search Donors ----------------
@app.route('/search', methods=['GET'])
def search_donor():
    try:
        name_query = request.args.get('name', '').lower()
        blood_query = request.args.get('blood_type', '').upper()
        results = []

        cursor.execute("SELECT * FROM donors")
        donor_rows = cursor.fetchall()
        for row in donor_rows:
            donor = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3],
                "blood_group": row[4],
                "phone": row[5],
                "location": row[6],
                "last_donated": str(row[7]) if len(row) > 7 and row[7] else None
            }
            if (name_query and name_query in donor['name'].lower()) or \
               (blood_query and blood_query == donor.get('blood_group', '').upper()):
                results.append(donor)
        return jsonify(results), 200
    except Exception as e:
        print("❌ Error in search_donor:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
@app.route('/donors/<blood_type>', methods=['GET'])
def get_donors_by_blood(blood_type):
    try:
        import urllib.parse
        decoded_blood_type = urllib.parse.unquote(blood_type)
        cursor.execute("SELECT * FROM donors WHERE UPPER(blood_group) = %s", (decoded_blood_type.upper(),))
        result = cursor.fetchall()
        donors = []
        for row in result:
            donors.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3],
                "blood_group": row[4],
                "phone": row[5],
                "location": row[6],
                "last_donated": str(row[7]) if len(row) > 7 and row[7] else None
            })
        return jsonify(donors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
