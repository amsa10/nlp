// app.js
document.getElementById("submit-btn").addEventListener("click", async function () {
    const userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    // Display user input
    addMessage(userInput, "user-message");

    // Send request to backend (FastAPI)
    const response = await fetch("/generate-report/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic: userInput }),
    });

    const data = await response.json();

    // Display AI response
    addMessage(data.report, "ai-message");
    document.getElementById("user-input").value = "";
});

function addMessage(content, type) {
    const chatBox = document.getElementById("chat-box");
    const message = document.createElement("div");
    message.classList.add("message", type);
    message.innerHTML = content;
    chatBox.appendChild(message);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}
