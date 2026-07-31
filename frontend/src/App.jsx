import { useState } from "react";
import API from "./services/api";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // User message add
    const userMessage = {
      role: "You",
      text: message,
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentMessage = message;
    setMessage("");
    setLoading(true);

    try {
      const res = await API.post("/chat", {
        message: currentMessage,
      });

      const aiMessage = {
        role: "Project Z",
        text: res.data.reply,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "Project Z",
          text: "❌ Error connecting backend.",
        },
      ]);

      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "40px auto",
        padding: "20px",
        fontFamily: "Arial",
      }}
    >
      <h1>🤖 Project Z</h1>

      <div
        style={{
          border: "1px solid #ccc",
          minHeight: "400px",
          padding: "15px",
          marginBottom: "20px",
          overflowY: "auto",
        }}
      >
        {messages.length === 0 && (
          <p>Start a conversation with Project Z.</p>
        )}

        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: "15px" }}>
            <strong>{msg.role}:</strong>
            <br />
            {msg.text}
          </div>
        ))}

        {loading && (
          <p>
            <strong>Project Z:</strong> Thinking...
          </p>
        )}
      </div>

      <input
        type="text"
        placeholder="Type your message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{
          width: "80%",
          padding: "10px",
          fontSize: "16px",
        }}
      />

      <button
        onClick={sendMessage}
        disabled={loading}
        style={{
          padding: "10px 20px",
          marginLeft: "10px",
        }}
      >
        {loading ? "Thinking..." : "Send"}
      </button>
    </div>
  );
}

export default App;