# Notify Donors – Blood Donation Web Application

## Description
Notify Donors is a web application where a user can be a **donor** or a **patient**. If you want to donate blood, you can register as a donor. Patients can request blood, and when a matching blood group is found, donors receive **email notifications** with the patient’s details. Users can also **search for donors** and **take a quiz** to learn more about blood donation.

## Features
- **User Roles:**  
  - **Donor:** Register to donate blood and receive notifications.  
  - **Patient:** Request blood and get matched with available donors.  
- **Email Notifications:** Donors get notified when a patient with a matching blood group requests blood.  
- **Donor Search:** Patients can search for donors by blood group.  
- **Educational Quiz:** Users can take a quiz to learn about blood donation.  
- **Responsive Design:** Easy-to-use interface on desktop.

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Flask
- **Database:** MySQL  
- **Notifications:** Email alerts  

## How It Works
1. Users register as either a **donor** or a **patient**.  
2. Patients submit blood requests specifying blood group and details.  
3. The system matches donors with the requested blood group.  
4. Donors receive email notifications with patient information.  
5. Patients can also search for donors manually.  
6. Users can take an educational quiz about blood.  

## Future Enhancements
- Mobile app integration for instant notifications.  
- SMS notifications for donors.    

## Usage
1. Clone the repository.  
2. Install dependencies using `pip install -r requirements.txt`.  
3. Configure MySQL database and update credentials in the Flask app.  
4. Start the Flask server with `python app.py` (or `flask run`).  
5. Open the application in your browser.
