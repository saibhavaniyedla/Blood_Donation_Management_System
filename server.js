const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');

const app = express();
const PORT = 5000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Database connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',   // your MySQL password if set
  database: 'blood_donation'
});

db.connect(err => {
  if (err) {
    console.error('❌ Database connection failed:', err);
    return;
  }
  console.log('✅ Connected to MySQL');
});

// Example route
app.get('/', (req, res) => {
  res.send('Hello from Blood Donation Backend');
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
