// =============================
// JWT Authentication Script
// =============================

// LOGIN FUNCTION
async function loginUser(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/api/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            // Save tokens
            localStorage.setItem("access_token", data.access);
            localStorage.setItem("refresh_token", data.refresh);
            localStorage.setItem("user_role", data.role);

            // Redirect based on role
            if (data.role === "admin") {
                window.location.href = "/admin-dashboard/";
            } else {
                window.location.href = "/student-dashboard/";
            }

        } else {
            alert(data.error || "Login failed");
        }

    } catch (error) {
        console.error("Login error:", error);
    }
}



// =============================
// GET AUTH HEADER
// =============================
function getAuthHeader() {

    const token = localStorage.getItem("access_token");

    return {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    };
}



// =============================
// API REQUEST WITH JWT
// =============================
async function apiRequest(url, method = "GET", body = null) {

    const options = {
        method: method,
        headers: getAuthHeader()
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    // If token expired try refresh
    if (response.status === 401) {
        const newToken = await refreshToken();

        if (newToken) {
            return apiRequest(url, method, body);
        }
    }

    return response.json();
}



// =============================
// REFRESH TOKEN
// =============================
async function refreshToken() {

    const refresh = localStorage.getItem("refresh_token");

    if (!refresh) {
        logoutUser();
        return null;
    }

    const response = await fetch("/api/token/refresh/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            refresh: refresh
        })
    });

    const data = await response.json();

    if (response.ok) {

        localStorage.setItem("access_token", data.access);
        return data.access;

    } else {

        logoutUser();
        return null;
    }
}



// =============================
// LOGOUT
// =============================
function logoutUser() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_role");

    window.location.href = "/login/";
}



// =============================
// PROTECTED API EXAMPLE
// =============================
async function loadStudentDashboard() {

    const data = await apiRequest("/api/student/dashboard/");

    console.log(data);

}

