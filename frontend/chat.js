async function loadChatHistory() {
    try {
        const response = await fetch("http://127.0.0.1:5000/chat-history");
        if (!response.ok) throw new Error("Failed to fetch chat history");
        
        const chats = await response.json();
        let chatContainer = document.getElementById("chat-box");
        chatContainer.innerHTML = "";

        if (chats.length === 0) {
            chatContainer.innerHTML = "<p>No chat history available.</p>";
            return;
        }

        chats.forEach((chat, index) => {
            let chatMessage = document.createElement("div");
            chatMessage.classList.add("chat-message");
            chatMessage.innerHTML = `<strong>${chat.user}</strong>: ${chat.message} 
                <small class="timestamp">(${chat.date})</small>`;
            
            // Delay animation for a stacked effect
            chatMessage.style.animationDelay = `${index * 0.1}s`;
            chatContainer.appendChild(chatMessage);
        });
        
        chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll to latest message
    } catch (error) {
        console.error("Error loading chat history:", error);
    }
}

async function sendMessage() {
    let user = document.getElementById("username").value.trim();
    let message = document.getElementById("message").value.trim();

    if (!user || !message) {
        alert("Please enter a username and message.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/chat-history", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user, message })
        });
        
        if (!response.ok) throw new Error("Failed to send message");
        
        document.getElementById("message").value = "";
        loadChatHistory();
    } catch (error) {
        console.error("Error sending message:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadChatHistory();

    document.getElementById("message").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
