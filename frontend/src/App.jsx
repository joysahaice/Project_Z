import { useState, useRef, useEffect } from "react";
import API from "./services/api";
import "./styles/chat.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
  chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages, loading]);

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
    <div className="container">
      <h1 className="title">🤖 Project Z</h1>

      <div className="chat-box">
        {messages.length === 0 && (
          <p>Start a conversation with Project Z...</p>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.role === "You" ? "user" : "ai"}`}
          >
            <div className="bubble">
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message ai">
            <div className="bubble">
              🤖 Thinking...
            </div>
          </div>
        )}

        <div ref={chatEndRef}></div>
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );

}

export default App;