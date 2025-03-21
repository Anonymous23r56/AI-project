document.addEventListener("DOMContentLoaded", function () {
    // Ensure the form exists before adding the event listener
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent page refresh
            
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("http://127.0.0.1:5000/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();
                console.log("Response:", data); // Debugging

                if (response.ok) {
                    alert("Login successful!");
                    console.log("Redirecting to dashboard...");
                    localStorage.setItem("isLoggedIn", "true"); // Store login state
                    window.location.href = "dashboard.html"; // Redirect to dashboard
                } else {
                    alert("Login failed: " + data.message);
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while logging in.");
            }
        });
    }

    // ✅ Logout Event Listener (This should be OUTSIDE login function)
    const logoutButton = document.getElementById("logout");
    if (logoutButton) {
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("isLoggedIn"); // Remove login session
            window.location.href = "index.html"; // Redirect to login page
        });
    }
});
