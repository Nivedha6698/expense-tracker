// TOKEN
function getToken() {
    return localStorage.getItem("token");
}

// ---------------- TOAST ----------------
function showToast(message, success = true) {
    let toast = document.getElementById("toast");

    if (!toast) return;

    toast.innerText = message;
    toast.style.background = success ? "#28a745" : "#dc3545";
    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}

// ---------------- LOGOUT ----------------
function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

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
            alert("Login failed ❌");
        }
    })
    .catch(() => alert("Server error"));
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
        alert("Signup successful ✅");
        window.location.href = "/";
    })
    .catch(() => alert("Signup failed"));
}

// ---------------- ADD EXPENSE ----------------
function addExpense() {
    let amount = document.getElementById('amount').value;

    if (!amount) {
        showToast("Amount required ❗", false);
        return;
    }

    fetch('/expenses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({
            amount: parseFloat(amount),
            category: document.getElementById('category').value,
            notes: document.getElementById('notes').value
        })
    })
    .then(res => {
        if (res.status === 401) {
            showToast("Unauthorized ❌ Please login again", false);
            logout();
            return;
        }
        return res.json();
    })
    .then(() => {
        showToast("Expense Added ✅");
        clearFields();
        loadExpenses();
    })
    .catch(() => showToast("Error adding expense ❌", false));
}

// ---------------- LOAD EXPENSES ----------------
function loadExpenses() {
    fetch('/expenses', {
        headers: {
            'Authorization': 'Bearer ' + getToken()
        }
    })
    .then(res => {
        if (res.status === 401) {
            showToast("Session expired ❌", false);
            logout();
            return;
        }
        return res.json();
    })
    .then(data => {
        if (!data) return;

        let list = document.getElementById("expenseList");
        if (!list) return;

        list.innerHTML = "";

        data.forEach(exp => {
            let li = document.createElement("li");

            li.innerHTML = `
                <span>${exp.amount} - ${exp.category} - ${exp.notes}</span>
                <div class="actions">
                    <button onclick="editExpense(${exp.id}, '${exp.amount}', '${exp.category}', \`${exp.notes}\`)">Edit</button>
                    <button onclick="deleteExpense(${exp.id})">Delete</button>
                </div>
            `;

            list.appendChild(li);
        });
    });
}

// ---------------- EDIT ----------------
function editExpense(id, amount, category, notes) {
    document.getElementById('expenseId').value = id;
    document.getElementById('amount').value = amount;
    document.getElementById('category').value = category;
    document.getElementById('notes').value = notes;
}

// ---------------- UPDATE ----------------
function updateExpense() {
    let id = document.getElementById('expenseId').value;

    if (!id) {
        showToast("Select expense to update ❗", false);
        return;
    }

    fetch(`/expenses/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({
            amount: document.getElementById('amount').value,
            category: document.getElementById('category').value,
            notes: document.getElementById('notes').value
        })
    })
    .then(res => {
        if (res.status === 401) {
            showToast("Unauthorized ❌", false);
            logout();
            return;
        }
        return res.json();
    })
    .then(() => {
        showToast("Updated successfully ✅");
        clearFields();
        loadExpenses();
    })
    .catch(() => showToast("Update failed ❌", false));
}

// ---------------- DELETE ----------------
function deleteExpense(id) {
    fetch(`/expenses/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + getToken()
        }
    })
    .then(res => {
        if (res.status === 401) {
            showToast("Unauthorized ❌", false);
            logout();
            return;
        }
    })
    .then(() => {
        showToast("Deleted 🗑️");
        loadExpenses();
    })
    .catch(() => showToast("Delete failed ❌", false));
}
// ---------------- EXPORT CSV ----------------
function exportCSV() {
    fetch('/expenses/export', {
        headers: {
            'Authorization': 'Bearer ' + getToken()
        }
    })
    .then(res => {
        if (res.status === 401) {
            showToast("Unauthorized ❌", false);
            logout();
            return;
        }
        return res.blob();
    })
    .then(blob => {
        if (!blob) return;

        const url = window.URL.createObjectURL(blob);
        window.open(url);
        showToast("Download started 📥");
    })
    .catch(() => showToast("Error exporting ❌", false));
}

// ---------------- CLEAR INPUTS ----------------
function clearFields() {
    document.getElementById('expenseId').value = "";
    document.getElementById('amount').value = "";
    document.getElementById('category').value = "";
    document.getElementById('notes').value = "";
}

// ---------------- AUTO LOAD ----------------
if (window.location.pathname === "/dashboard") {
    loadExpenses();
}