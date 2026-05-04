import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi, I’m AcquisAI. How can I help today?",
      sources: [],
    },
  ]);

  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const currentInput = input;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentInput,
        sources: [],
      },
    ]);

    setInput("");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: currentInput }),
      });

      const data = await res.json();
      console.log("Backend response:", data);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: data.answer || "No answer returned.",
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Error connecting to server.",
          sources: [],
        },
      ]);
    }
  };

  return (
    <main className="app">
      <header className="header">
        <div className="brand">AcquisAI</div>
      </header>

      <section className="chat">
        <div className="intro">
          <h1>Your EU Treaty Intelligence Assistant</h1>
          <p>Ask questions across treaties, protocols, and legal provisions.</p>
        </div>

        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <div className="bubble">{msg.text}</div>

              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  {msg.sources.map((s, i) => (
                    <div key={i} className="source-card">
                      <div className="file">{s.file_name}</div>
                      <div className="pages">
                        Pages: {s.pages.join(", ")}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      <div className="composer">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Message AcquisAI..."
        />
        <button onClick={sendMessage}>↑</button>
      </div>
    </main>
  );
}

export default App;