import { useState } from "react";
import { sendMessage } from "./api";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sessionId = localStorage.getItem("sessionId") || 
    Math.random().toString(36).substring(7);

  localStorage.setItem("sessionId", sessionId);

  async function handleSend() {
    const userMessage = { role: "user", text: input };
    setMessages([...messages, userMessage]);

    const response = await sendMessage(input, sessionId);

    setMessages(prev => [...prev, 
      { role: "assistant", text: response.reply }
    ]);

    setInput("");
  }

  return (
    <div>
      {messages.map((msg, index) => (
        <div key={index}>
          <b>{msg.role}:</b> {msg.text}
        </div>
      ))}
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default Chat;