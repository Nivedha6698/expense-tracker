let token = localStorage.getItem("token");

// ---------------- LOGIN ----------------
function login() {
    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "/dashboard";
        } else {
            alert("Login failed");
        }
    });
}

// ---------------- SIGNUP ----------------
function signup() {
    fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        })
    })
    .then(res => res.json())
    .then(() => {
        alert("Signup successful");
        window.location.href = "/";
    });
}

// ---------------- ADD EXPENSE ----------------
function addExpense() {
    fetch('/expenses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem("token")
        },
        body: JSON.stringify({
            amount: parseFloat(document.getElementById('amount').value),  // fix
            category: document.getElementById('category').value,
            notes: document.getElementById('notes').value
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        loadExpenses();
    });
}
// ---------------- LOAD EXPENSES ----------------
function loadExpenses() {
    fetch('/expenses', {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem("token")
        }
    })
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("expenseList");
        list.innerHTML = "";

        data.forEach(exp => {
            let li = document.createElement("li");
            li.innerHTML = `
                ${exp.amount} - ${exp.category} - ${exp.notes}
                <button onclick="editExpense(${exp.id}, '${exp.amount}', '${exp.category}', '${exp.notes}')">Edit</button>
                <button onclick="deleteExpense(${exp.id})">Delete</button>
            `;
            list.appendChild(li);
        });
    });
}
function editExpense(id, amount, category, notes) {
    document.getElementById('expenseId').value = id;
    document.getElementById('amount').value = amount;
    document.getElementById('category').value = category;
    document.getElementById('notes').value = notes;
}

function updateExpense() {
    let id = document.getElementById('expenseId').value;

    fetch(`/expenses/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem("token")
        },
        body: JSON.stringify({
            amount: document.getElementById('amount').value,
            category: document.getElementById('category').value,
            notes: document.getElementById('notes').value
        })
    })
    .then(res => res.json())
    .then(() => {
        alert("Updated!");
        loadExpenses();
    });
}
// ---------------- DELETE ----------------
function deleteExpense(id) {
    fetch(`/expenses/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem("token")
        }
    })
    .then(() => loadExpenses());
}

// ---------------- SUMMARY ----------------
function loadSummary() {
    fetch('/expenses/summary', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("summaryList");
        list.innerHTML = "";

        for (let category in data) {
            let li = document.createElement("li");
            li.innerText = `${category} : ₹${data[category]}`;
            list.appendChild(li);
        }
    });
}

// ---------------- EXPORT CSV ----------------
function exportCSV() {
    fetch('/expenses/export', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.download_url) {
            window.open(data.download_url, '_blank'); // open S3 link
        } else {
            alert("Export failed");
        }
    });
}


// Load expenses on dashboard
if (window.location.pathname === "/dashboard") {
    loadExpenses();
}