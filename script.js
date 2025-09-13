const API_URL = "http://localhost:5000";

// Donor registration
if (document.getElementById("donorForm")) {
  document.getElementById("donorForm").onsubmit = async (e) => {
    e.preventDefault();
    const donor = {
      name: document.getElementById("donorName").value,
      age: document.getElementById("donorAge").value,
      blood_group: document.getElementById("donorBlood").value,
      phone: document.getElementById("donorPhone").value,
      location: document.getElementById("donorLocation").value,
    };
    const res = await fetch(`${API_URL}/donors`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(donor),
    });
    const data = await res.json();
    if (res.ok) {
      alert("✅ Donor Registered Successfully!");
    } else {
      alert(data.error || "Registration failed.");
    }
  };
}

// Blood request
if (document.getElementById("requestForm")) {
  document.getElementById("requestForm").onsubmit = async (e) => {
    e.preventDefault();
    const reqData = {
      name: document.getElementById("reqName").value,
      blood_group: document.getElementById("reqBlood").value,
      phone: document.getElementById("reqPhone").value,
      location: document.getElementById("reqLocation").value,
    };
    const res = await fetch(`${API_URL}/requests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reqData),
    });
    if (res.ok) {
      alert("📩 Blood Request Submitted!");
    } else {
      alert("Request failed.");
    }
  };
}

// Search donors
if (document.getElementById("searchForm")) {
  document.getElementById("searchForm").onsubmit = async (e) => {
    e.preventDefault();
    const blood_group = document.getElementById("searchBlood").value;
    const res = await fetch(`${API_URL}/donors/${blood_group}`);
    const donors = await res.json();

    const resultsDiv = document.getElementById("results");
    if (donors.length === 0) {
      resultsDiv.innerHTML = "<p>❌ No donors found</p>";
    } else {
      // Create table header
      let table = `<table border='1' style='width:100%;border-collapse:collapse;'>
        <tr>
          <th>Name</th>
          <th>Age</th>
          <th>Blood Group</th>
          <th>Phone</th>
          <th>Location</th>
          <th>Last Donated</th>
        </tr>`;
      // Add donor rows
      table += donors.map(d => `
        <tr>
          <td>${d.name}</td>
          <td>${d.age}</td>
          <td>${d.blood_group}</td>
          <td>${d.phone}</td>
          <td>${d.location}</td>
          <td>${d.last_donated ? d.last_donated : 'Never'}</td>
        </tr>`).join("");
      table += "</table>";
      resultsDiv.innerHTML = table;
    }
  };

  // Fetch and display blood inventory on page load
  window.addEventListener('DOMContentLoaded', async () => {
    const invDiv = document.getElementById('inventory');
    if (invDiv) {
      const res = await fetch(`${API_URL}/blood_inventory`);
      const inventory = await res.json();
      if (inventory.length === 0) {
        invDiv.innerHTML = '<p>No blood units in hospital.</p>';
      } else {
        let table = `<table border='1' style='width:100%;border-collapse:collapse;'>
          <tr><th>Blood Group</th><th>Units Available</th></tr>`;
        table += inventory.map(b => `
          <tr><td>${b.blood_group}</td><td>${b.units}</td></tr>
        `).join("");
        table += "</table>";
        invDiv.innerHTML = table;
      }
    }
  });
}
