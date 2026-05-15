import { useState } from "react";
import Layout from "../components/layout/Layout";

function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! Ask me about your contract." }
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    
    const userMessage = { sender: "user", text: input };

    
    const botMessage = {
      sender: "bot",
      text: "This is a sample response. Backend will answer here."
    };

    setMessages([...messages, userMessage, botMessage]);
    setInput("");
  };


  //whithout cover space
//   return (
//     <Layout>
//       <h2 className="text-3xl font-bold mb-6 text-center">
//         Contract Chatbot
//       </h2>

//       {/* Chat Container */}
//       <div className="max-w-3xl mx-auto flex flex-col h-[70vh] border rounded-lg shadow">

//         {/* Messages */}
//         <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
//           {messages.map((msg, index) => (
//             <div
//               key={index}
//               className={`flex ${
//                 msg.sender === "user" ? "justify-end" : "justify-start"
//               }`}
//             >
//               <div
//                 className={`px-4 py-2 rounded-lg max-w-xs ${
//                   msg.sender === "user"
//                     ? "bg-blue-500 text-white"
//                     : "bg-white border"
//                 }`}
//               >
//                 {msg.text}
//               </div>
//             </div>
//           ))}
//         </div>

//         {/* Input Box */}
//         <div className="p-3 border-t flex gap-2">
//        <textarea
//   className="flex-1 border rounded px-3 py-2 outline-none resize-none min-h-[32px] max-h-24 overflow-y-auto"
//   placeholder="Ask about contract..."
//   value={input}
//   onChange={(e) => setInput(e.target.value)}
  
//    rows={1} 

//   onInput={(e) => {
//     e.target.style.height = "auto";
//     e.target.style.height = Math.min(e.target.scrollHeight, 96) + "px";
//   }}

//   onKeyDown={(e) => {
//     if (e.key === "Enter" && !e.shiftKey) {
//       e.preventDefault();
//       handleSend();
//     }
//   }}
// />
//           <button
//             onClick={handleSend}
//              className="bg-blue-600 hover:bg-blue-700 text-white px-4 h-[28px] rounded flex items-center justify-center self-end"
//   >
//             Send
//           </button>
//         </div>
//       </div>
//     </Layout>
//   );
// }

// export default Chatbot;



//cover space 
// return (
//   <Layout>
//     <h2 className="text-3xl font-bold mb-6 text-center">
//       Contract Chatbot
//     </h2>

//     {/* Chat Container */}
//     <div className="w-full h-[80vh] flex justify-center">
//       <div className="w-full max-w-5xl flex flex-col border rounded-lg shadow bg-white">

//         {/* Messages */}
//         <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
//           {messages.map((msg, index) => (
//             <div
//               key={index}
//               className={`flex ${
//                 msg.sender === "user" ? "justify-end" : "justify-start"
//               }`}
//             >
//               <div
//                 className={`px-4 py-2 rounded-lg max-w-xs ${
//                   msg.sender === "user"
//                     ? "bg-blue-500 text-white"
//                     : "bg-white border"
//                 }`}
//               >
//                 {msg.text}
//               </div>
//             </div>
//           ))}
//         </div>

//         {/* Input Box */}
//         <div className="p-3 border-t flex items-end gap-2">
          
//           {/* TEXTAREA */}
//           <textarea
//             className="flex-1 border rounded px-3 py-2 outline-none resize-none min-h-[32px] max-h-24 overflow-y-auto"
//             placeholder="Ask about contract..."
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             rows={1}
//             onInput={(e) => {
//               e.target.style.height = "auto";
//               e.target.style.height =
//                 Math.min(e.target.scrollHeight, 96) + "px";
//             }}
//             onKeyDown={(e) => {
//               if (e.key === "Enter" && !e.shiftKey) {
//                 e.preventDefault();
//                 handleSend();
//               }
//             }}
//           />

//           {/* SEND BUTTON */}
//           <button
//             onClick={handleSend}
//             className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded flex items-center justify-center h-[34px]"
//           >
//             Send
//           </button>

//         </div>
//       </div>
//     </div>
//   </Layout>
// );
// }

// export default Chatbot;


// almost 
// return (
//   <Layout fullWidth={true}>
//     <h2 className="text-3xl font-bold mb-6 text-center">
//       Contract Chatbot
//     </h2>

//     {/* Chat Container */}
//     <div className="w-full h-[80vh]">
//       <div className="w-full h-full flex flex-col border bg-white">

//         {/* Messages */}
//         <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
//           {messages.map((msg, index) => (
//             <div
//               key={index}
//               className={`flex ${
//                 msg.sender === "user" ? "justify-end" : "justify-start"
//               }`}
//             >
//               <div
//                 className={`px-4 py-2 rounded-lg max-w-xs ${
//                   msg.sender === "user"
//                     ? "bg-blue-500 text-white"
//                     : "bg-white border"
//                 }`}
//               >
//                 {msg.text}
//               </div>
//             </div>
//           ))}
//         </div>

//         {/* Input Box */}
//         <div className="p-3 border-t flex items-end gap-2">
//           <textarea
//             className="flex-1 border rounded px-3 py-2 outline-none resize-none min-h-[32px] max-h-24 overflow-y-auto"
//             placeholder="Ask about contract..."
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             rows={1}
//             onInput={(e) => {
//               e.target.style.height = "auto";
//               e.target.style.height =
//                 Math.min(e.target.scrollHeight, 96) + "px";
//             }}
//             onKeyDown={(e) => {
//               if (e.key === "Enter" && !e.shiftKey) {
//                 e.preventDefault();
//                 handleSend();
//               }
//             }}
//           />

//           <button
//             onClick={handleSend}
//             className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded flex items-center justify-center h-[34px]"
//           >
//             Send
//           </button>
//         </div>

//       </div>
//     </div>
//   </Layout>
// );
// }

// export default Chatbot;



//DONEEEEEEEEEEEEEEEE
// return (
//   <Layout fullWidth={true}>
    
//     {/* FULL PAGE CONTAINER */}
//     <div className="flex flex-col h-[calc(100vh-64px)]">
      
//       {/* HEADER */}
//       <div className="flex items-center justify-center h-16 bg-gray-100 border-b">
//         <h2 className="text-3xl font-bold">
//           Contract Chatbot
//         </h2>
//       </div>

//       {/* CHAT AREA */}
//       <div className="flex-1 flex flex-col bg-white">

//         {/* Messages */}
//         <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
//           {messages.map((msg, index) => (
//             <div
//               key={index}
//               className={`flex ${
//                 msg.sender === "user" ? "justify-end" : "justify-start"
//               }`}
//             >
//               <div
//                 className={`px-4 py-2 rounded-lg max-w-xs ${
//                   msg.sender === "user"
//                     ? "bg-blue-500 text-white"
//                     : "bg-white border"
//                 }`}
//               >
//                 {msg.text}
//               </div>
//             </div>
//           ))}
//         </div>

//         {/* INPUT */}
//         <div className="p-3 border-t flex items-end gap-2 bg-white">
//           <textarea
//             className="flex-1 border rounded px-3 py-2 outline-none resize-none min-h-[32px] max-h-24 overflow-y-auto"
//             placeholder="Ask about contract..."
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             rows={1}
//             onInput={(e) => {
//               e.target.style.height = "auto";
//               e.target.style.height =
//                 Math.min(e.target.scrollHeight, 96) + "px";
//             }}
//             onKeyDown={(e) => {
//               if (e.key === "Enter" && !e.shiftKey) {
//                 e.preventDefault();
//                 handleSend();
//               }
//             }}
//           />

//           <button
//             onClick={handleSend}
//             className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded flex items-center justify-center h-[34px]"
//           >
//             Send
//           </button>
//         </div>

//       </div>
//     </div>

//   </Layout>
// );
// }

// export default Chatbot;

return (
  <Layout fullWidth={true}>
    
    {/* FULL PAGE */}
    <div className="flex flex-col h-[calc(100vh-64px)]">

      {/* HEADER BAR (FULL WIDTH, NO GAP) */}
      <div className="w-full h-16 flex items-center justify-center bg-white border-b">
        <h2 className="text-2xl font-bold">
          Contract Chatbot
        </h2>
      </div>

      {/* CHAT AREA */}
      <div className="flex-1 flex flex-col bg-white">

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`px-4 py-2 rounded-lg max-w-xs ${
                  msg.sender === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-white border"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        {/* INPUT */}
        <div className="p-3 border-t flex items-end gap-2 bg-white">
          <textarea
            className="flex-1 border rounded px-3 py-2 outline-none resize-none min-h-[32px] max-h-24 overflow-y-auto"
            placeholder="Ask about contract..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={1}
            onInput={(e) => {
              e.target.style.height = "auto";
              e.target.style.height =
                Math.min(e.target.scrollHeight, 96) + "px";
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />

          <button
            onClick={handleSend}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded flex items-center justify-center h-[34px]"
          >
            Send
          </button>
        </div>

      </div>
    </div>

  </Layout>
);
}

export default Chatbot;