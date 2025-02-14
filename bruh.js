{/* Smart Home Controls */}
<div className="flex flex-col items-end gap-6 mt-6 absolute left-10 top-20">
  {/* Light Control */}
  <motion.div
    className="p-6 bg-[#1a2332] rounded-2xl shadow-lg"
    whileHover={{ scale: 1.05 }}
  >
    <h2 className="text-lg font-semibold mb-3">Light Control</h2>
    <button
      className={`btn ${
        areLightsOn ? "bg-green-500" : "bg-gray-500"
      }`}
      onClick={() => setAreLightsOn(!areLightsOn)}
    >
      Toggle Lights
    </button>
  </motion.div>

  {/* Fan Control */}
  <motion.div
    className="p-6 bg-[#1a2332] rounded-2xl shadow-lg"
    whileHover={{ scale: 1.05 }}
  >
    <h2 className="text-lg font-semibold mb-3">Fan Control</h2>
    <button
      className={`btn ${isFanOn ? "bg-green-500" : "bg-gray-500"}`}
      onClick={() => setIsFanOn(!isFanOn)}
    >
      Toggle Fan
    </button>
  </motion.div>

{/* Chat Interface */}
<div className="mt-6 w-full max-w-lg p-4 bg-[#1a2332] rounded-2xl shadow-lg flex flex-col">
  <div className="h-48 overflow-y-auto p-3 bg-gray-900 rounded-lg">
    {messages.map((msg, index) => (
      <p
        key={index}
        className={`mb-2 p-2 rounded-lg ${
          msg.sender === "user" ? "bg-blue-500" : "bg-gray-700"
        }`}
      >
        {msg.text}
      </p>
    ))}
    {isTyping && <p className="text-gray-400">Typing...</p>}
  </div>
  <div className="mt-3 flex">
    <input
      className="flex-1 p-2 bg-gray-800 rounded-l-lg focus:outline-none"
      type="text"
      value={input}
      onChange={(e) => setInput(e.target.value)}
      placeholder="Type a message..."
    />
    <button
      onClick={sendMessage}
      className="bg-blue-500 px-4 py-2 rounded-r-lg"
    >
      Send
    </button>
  </div>
</div>
</div>