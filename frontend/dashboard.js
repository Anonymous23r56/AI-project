document.addEventListener("DOMContentLoaded", async function () {
    if (!localStorage.getItem("isLoggedIn")) {
        window.location.href = "index.html";
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/users");
        const data = await response.json();

        if (data.users.length > 0) {
            const user = data.users[0]; // Get logged-in user
            document.getElementById("userName").textContent = user.username;
            document.getElementById("userEmail").textContent = user.email;
            document.getElementById("userDiagnosis").textContent = user.diagnosis || "No records yet"; 
        }
    } catch (error) {
        console.error("Error fetching user data:", error);
    }

    // Logout Function
    document.getElementById("logout").addEventListener("click", function () {
        localStorage.removeItem("isLoggedIn");
        window.location.href = "index.html";
    });

    // Dark Mode Toggle
    const toggleButton = document.createElement("button");
    toggleButton.textContent = "🌙 Dark Mode";
    toggleButton.classList.add("dark-mode-toggle");
    document.body.appendChild(toggleButton);

    toggleButton.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        toggleButton.textContent = document.body.classList.contains("dark-mode") ? "☀️ Light Mode" : "🌙 Dark Mode";
    });

    // Fetch and Display Chat History
    try {
        const response = await fetch("http://127.0.0.1:5000/chat-history");
        const data = await response.json();

        const chatList = document.getElementById("chatList");
        chatList.innerHTML = ""; // Clear previous content

        if (data.length > 0) {
            data.forEach(chat => {
                const chatItem = document.createElement("div");
                chatItem.classList.add("chat-item");
                chatItem.textContent = `🗓️ ${chat.date} - ${chat.message}`;
                chatItem.addEventListener("click", function () {
                    window.location.href = `chat.html?chat_id=${chat.id}`;
                });
                chatList.appendChild(chatItem);
            });
        } else {
            chatList.innerHTML = "<p>No chat history available.</p>";
        }
    } catch (error) {
        console.error("Error fetching chat history:", error);
    }

    // AI Chat Button
    const aiChatButton = document.createElement("button");
    aiChatButton.textContent = "🤖 AI Chat";
    aiChatButton.classList.add("ai-chat-btn");
    document.body.appendChild(aiChatButton);

    aiChatButton.addEventListener("click", function () {
        window.location.href = "chat.html";
    });
});
