// import { useState } from "react";
// import Layout from "../components/layout/Layout";

// function Chatbot() {
//   const [messages, setMessages] = useState([
//     { sender: "bot", text: "Hello! Ask me about your contract." }
//   ]);
//   const [input, setInput] = useState("");

//   const handleSend = () => {
//     if (!input.trim()) return;

    
//     const userMessage = { sender: "user", text: input };

    
//     const botMessage = {
//       sender: "bot",
//       text: "This is a sample response. Backend will answer here."
//     };

//     setMessages([...messages, userMessage, botMessage]);
//     setInput("");
//   };


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




// import { useState } from "react";
// import Layout from "../components/layout/Layout";

// function Chatbot() {
//   const [messages, setMessages] = useState([
//     { sender: "bot", text: "Hello! Ask me about your contract." }
//   ]);
//   const [input, setInput] = useState("");

//   const handleSend = () => {
//     if (!input.trim()) return;

    
//     const userMessage = { sender: "user", text: input };

    
//     const botMessage = {
//       sender: "bot",
//       text: "This is a sample response. Backend will answer here."
//     };

//     setMessages([...messages, userMessage, botMessage]);
//     setInput("");
//   };



// return (
//   <Layout fullWidth={true}>
    
//     {/* FULL PAGE */}
//     <div className="flex flex-col h-[calc(100vh-64px)]">

//       {/* HEADER BAR (FULL WIDTH, NO GAP) */}
//       <div className="w-full h-16 flex items-center justify-center bg-white border-b">
//         <h2 className="text-2xl font-bold">
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


// week 3 fridayyyyy

// import { useState } from "react";
// import Layout from "../components/layout/Layout";
// import { chatWithContract } from "../services/api";

// function Chatbot() {
//   const [messages, setMessages] = useState([
//     { sender: "bot", text: "Hello! Ask me about your contract." },
//   ]);

//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleSend = async () => {
//     if (!input.trim()) return;

//     const userMessage = { sender: "user", text: input };
//     const question = input;

//     setMessages((prev) => [...prev, userMessage]);
//     setInput("");
//     setLoading(true);

//     try {
//       const data = await chatWithContract(question);

//       console.log("Chat response:", data);

//       const botMessage = {
//         sender: "bot",
//         text:
//           data.answer ||
//           data.response ||
//           data.message ||
//           "No response received.",
//       };

//       setMessages((prev) => [...prev, botMessage]);
//     } catch (error) {
//       console.log("Chat error:", error);

//       const errorMessage = {
//         sender: "bot",
//         text: "Backend unavailable. Please try again later.",
//       };

//       setMessages((prev) => [...prev, errorMessage]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <Layout fullWidth={true}>
//       <div className="flex flex-col h-[calc(100vh-64px)]">
//         <div className="w-full h-16 flex items-center justify-center bg-white border-b">
//           <h2 className="text-2xl font-bold">Contract Chatbot</h2>
//         </div>

//         <div className="flex-1 flex flex-col bg-white">
//           <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
//             {messages.map((msg, index) => (
//               <div
//                 key={index}
//                 className={`flex ${
//                   msg.sender === "user" ? "justify-end" : "justify-start"
//                 }`}
//               >
//                 <div
//                   className={`px-4 py-2 rounded-lg max-w-xs ${
//                     msg.sender === "user"
//                       ? "bg-blue-500 text-white"
//                       : "bg-white border"
//                   }`}
//                 >
//                   {msg.text}
//                 </div>
//               </div>
//             ))}

//             {loading && (
//               <div className="flex justify-start">
//                 <div className="px-4 py-2 rounded-lg max-w-xs bg-white border text-gray-500">
//                   Thinking...
//                 </div>
//               </div>
//             )}
//           </div>

//           <div className="p-3 border-t flex items-end gap-2 bg-white">
//             <textarea
//               className="flex-1 border rounded px-3 py-2 outline-none resize-none min-h-[32px] max-h-24 overflow-y-auto"
//               placeholder="Ask about contract..."
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               rows={1}
//               disabled={loading}
//               onInput={(e) => {
//                 e.target.style.height = "auto";
//                 e.target.style.height =
//                   Math.min(e.target.scrollHeight, 96) + "px";
//               }}
//               onKeyDown={(e) => {
//                 if (e.key === "Enter" && !e.shiftKey) {
//                   e.preventDefault();
//                   handleSend();
//                 }
//               }}
//             />

//             <button
//               onClick={handleSend}
//               disabled={loading}
//               className={`text-white px-4 py-1.5 rounded flex items-center justify-center h-[34px] ${
//                 loading
//                   ? "bg-gray-400 cursor-not-allowed"
//                   : "bg-blue-600 hover:bg-blue-700"
//               }`}
//             >
//               {loading ? "..." : "Send"}
//             </button>
//           </div>
//         </div>
//       </div>
//     </Layout>
//   );
// }

// export default Chatbot;



//week4 mondayyyyyy

// import { useEffect, useRef, useState } from "react";
// import Layout from "../components/layout/Layout";
// import { chatWithContract } from "../services/api";

// function Chatbot() {
//   const [messages, setMessages] = useState([
//     { sender: "bot", text: "Hello! Ask me about your contract." },
//   ]);

//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);

//   const messagesEndRef = useRef(null);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({
//       behavior: "smooth",
//     });
//   }, [messages, loading]);

//   const handleSend = async () => {
//     if (!input.trim()) return;

//     const userMessage = {
//       sender: "user",
//       text: input,
//     };

//     const question = input;

//     setMessages((prev) => [...prev, userMessage]);
//     setInput("");
//     setLoading(true);

//     try {
//       const data = await chatWithContract(question);

//       console.log("Chat response:", data);

//       const botMessage = {
//         sender: "bot",
//         text:
//           data.answer ||
//           data.response ||
//           data.message ||
//           "No response received.",
//       };

//       setMessages((prev) => [...prev, botMessage]);
//     } catch (error) {
//       console.log("Chat error:", error);

//       const errorMessage = {
//         sender: "bot",
//         text: "Backend unavailable. Please try again later.",
//       };

//       setMessages((prev) => [...prev, errorMessage]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const suggestedQuestions = [
//     "What is the termination clause?",
//     "Summarize payment obligations",
//     "Explain confidentiality clause",
//   ];

//   return (
//     <Layout fullWidth={true}>
//       <div className="flex flex-col h-[calc(100vh-64px)]">
//         {/* HEADER */}
//         <div className="w-full h-16 flex items-center justify-center bg-white border-b">
//           <h2 className="text-2xl font-bold">
//             Contract Chatbot
//           </h2>
//         </div>

//         {/* CHAT AREA */}
//         <div className="flex-1 flex flex-col bg-white">
//           <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50">
//             {messages.map((msg, index) => (
//               <div
//                 key={index}
//                 className={`flex ${
//                   msg.sender === "user"
//                     ? "justify-end"
//                     : "justify-start"
//                 }`}
//               >
//                 <div
//                   className={`px-4 py-3 rounded-xl w-fit max-w-2xl whitespace-pre-wrap leading-7 text-[15px] ${
//                     msg.sender === "user"
//                       ? "bg-blue-600 text-white"
//                       : "bg-white border text-gray-800 shadow-sm max-h-[400px] overflow-y-auto"
//                   }`}
//                 >
//                   {msg.text}
//                 </div>
//               </div>
//             ))}

//             {/* SUGGESTED QUESTIONS */}
//             {messages.length === 1 && !loading && (
//               <div className="flex flex-wrap gap-2 mt-2">
//                 {suggestedQuestions.map((question, index) => (
//                   <button
//                     key={index}
//                     onClick={() => setInput(question)}
//                     className="bg-white border text-gray-700 px-3 py-2 rounded-full text-sm hover:bg-gray-100"
//                   >
//                     {question}
//                   </button>
//                 ))}
//               </div>
//             )}

//             {/* TYPING LOADER */}
//             {loading && (
//               <div className="flex justify-start">
//                 <div className="px-4 py-3 rounded-xl bg-white border text-gray-500 shadow-sm">
//                   <span className="animate-pulse">
//                     Thinking...
//                   </span>
//                 </div>
//               </div>
//             )}

//             <div ref={messagesEndRef} />
//           </div>

//           {/* INPUT AREA */}
//           <div className="p-3 border-t bg-white">
//             <div className="flex items-end gap-2">
//               <textarea
//                 className="flex-1 border rounded-lg px-3 py-2 outline-none resize-none min-h-[38px] max-h-24 overflow-y-auto"
//                 placeholder="Ask about contract..."
//                 value={input}
//                 onChange={(e) => setInput(e.target.value)}
//                 rows={1}
//                 disabled={loading}
//                 onInput={(e) => {
//                   e.target.style.height = "auto";
//                   e.target.style.height =
//                     Math.min(e.target.scrollHeight, 96) + "px";
//                 }}
//                 onKeyDown={(e) => {
//                   if (e.key === "Enter" && !e.shiftKey) {
//                     e.preventDefault();
//                     handleSend();
//                   }
//                 }}
//               />

//               <button
//                 onClick={handleSend}
//                 disabled={loading}
//                 className={`text-white px-5 py-2 rounded-lg flex items-center justify-center h-[38px] ${
//                   loading
//                     ? "bg-gray-400 cursor-not-allowed"
//                     : "bg-blue-600 hover:bg-blue-700"
//                 }`}
//               >
//                 {loading ? "..." : "Send"}
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
//     </Layout>
//   );
// }

// export default Chatbot;














//imppppppppp
//week 4fridayyyyyyyyyyyyy
// import { useEffect, useRef, useState } from "react";
// import ReactMarkdown from "react-markdown";
// import Layout from "../components/layout/Layout";
// import {
//   chatWithContract,
//   getContracts,
// } from "../services/api";

// function Chatbot() {
//   const getTime = () =>
//     new Date().toLocaleTimeString([], {
//       hour: "2-digit",
//       minute: "2-digit",
//     });

//   const [messages, setMessages] = useState([
//     {
//       sender: "bot",
//       text: "Hello! Ask me about your contract.",
//       time: getTime(),
//       sources: [],
//     },
//   ]);

//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [contracts, setContracts] = useState([]);
//   const [selectedContractId, setSelectedContractId] = useState("");
//   const [darkMode, setDarkMode] = useState(false);
//   const [copiedIndex, setCopiedIndex] = useState(null);

//   const messagesEndRef = useRef(null);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({
//       behavior: "smooth",
//     });
//   }, [messages, loading]);

//   useEffect(() => {
//     const fetchContracts = async () => {
//       try {
//         const data = await getContracts();
//         setContracts(data || []);

//         if (data && data.length > 0) {
//           setSelectedContractId(data[0].contract_id);
//         }
//       } catch (error) {
//         console.log("Contracts fetch error:", error);
//       }
//     };

//     fetchContracts();
//   }, []);

//   const handleCopy = async (text, index) => {
//     try {
//       await navigator.clipboard.writeText(text);
//       setCopiedIndex(index);

//       setTimeout(() => {
//         setCopiedIndex(null);
//       }, 1500);
//     } catch (error) {
//       console.log("Copy failed:", error);
//     }
//   };

//   const handleSend = async () => {
//     if (!input.trim()) return;

//     if (!selectedContractId) {
//       setMessages((prev) => [
//         ...prev,
//         {
//           sender: "bot",
//           text: "Please select a contract first.",
//           time: getTime(),
//           sources: [],
//         },
//       ]);
//       return;
//     }

//     const question = input;

//     const userMessage = {
//       sender: "user",
//       text: input,
//       time: getTime(),
//       sources: [],
//     };

//     setMessages((prev) => [...prev, userMessage]);
//     setInput("");
//     setLoading(true);

//     try {
//       const data = await chatWithContract(
//         selectedContractId,
//         question
//       );

//       console.log("Chat response:", data);

//       const botMessage = {
//         sender: "bot",
//         text:
//           data.answer ||
//           data.response ||
//           data.message ||
//           "No response received.",
//         time: getTime(),
//         sources:
//           data.sources ||
//           data.citations ||
//           data.context ||
//           [],
//       };

//       setMessages((prev) => [...prev, botMessage]);
//     } catch (error) {
//       console.log("Chat error:", error);

//       const errorMessage = {
//         sender: "bot",
//         text: "Backend unavailable. Please try again later.",
//         time: getTime(),
//         sources: [],
//       };

//       setMessages((prev) => [...prev, errorMessage]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const suggestedQuestions = [
//     "What is the termination clause?",
//     "Summarize payment obligations",
//     "Explain confidentiality clause",
//   ];

//   return (
//     <Layout fullWidth={true}>
//       <div
//         className={`flex flex-col h-[calc(100vh-64px)] ${
//           darkMode ? "bg-gray-950 text-white" : "bg-white text-gray-900"
//         }`}
//       >
//         {/* HEADER */}
//         <div
//           className={`w-full h-16 flex items-center justify-between px-6 border-b ${
//             darkMode
//               ? "bg-gray-900 border-gray-700"
//               : "bg-white border-gray-200"
//           }`}
//         >
//           <h2 className="text-2xl font-bold">
//             Contract Chatbot
//           </h2>

//           <button
//             onClick={() => setDarkMode(!darkMode)}
//             className={`px-4 py-2 rounded-lg text-sm font-semibold ${
//               darkMode
//                 ? "bg-white text-gray-900"
//                 : "bg-gray-900 text-white"
//             }`}
//           >
//             {darkMode ? "Light Mode" : "Dark Mode"}
//           </button>
//         </div>

//         {/* CONTRACT SELECTOR */}
//         <div
//           className={`px-5 py-3 border-b ${
//             darkMode
//               ? "bg-gray-900 border-gray-700"
//               : "bg-white border-gray-200"
//           }`}
//         >
//           <label className="text-sm font-semibold mr-3">
//             Select Contract:
//           </label>

//           <select
//             value={selectedContractId}
//             onChange={(e) =>
//               setSelectedContractId(e.target.value)
//             }
//             className={`border rounded-lg px-3 py-2 text-sm outline-none ${
//               darkMode
//                 ? "bg-gray-800 text-white border-gray-600"
//                 : "bg-white text-gray-900 border-gray-300"
//             }`}
//           >
//             <option value="">Choose contract</option>

//             {contracts.map((contract) => (
//               <option
//                 key={contract.contract_id}
//                 value={contract.contract_id}
//               >
//                 {contract.filename || contract.contract_id}
//               </option>
//             ))}
//           </select>
//         </div>

//         {/* CHAT AREA */}
//         <div
//           className={`flex-1 flex flex-col ${
//             darkMode ? "bg-gray-950" : "bg-white"
//           }`}
//         >
//           <div
//             className={`flex-1 overflow-y-auto p-5 space-y-4 ${
//               darkMode ? "bg-gray-950" : "bg-gray-50"
//             }`}
//           >
//             {messages.map((msg, index) => (
//               <div
//                 key={index}
//                 className={`flex ${
//                   msg.sender === "user"
//                     ? "justify-end"
//                     : "justify-start"
//                 }`}
//               >
//                 <div
//                   className={`px-4 py-3 rounded-xl w-fit max-w-2xl leading-7 text-[15px] ${
//                     msg.sender === "user"
//                       ? "bg-blue-600 text-white"
//                       : darkMode
//                       ? "bg-gray-800 border border-gray-700 text-gray-100 shadow-sm max-h-[420px] overflow-y-auto"
//                       : "bg-white border text-gray-800 shadow-sm max-h-[420px] overflow-y-auto"
//                   }`}
//                 >
//                   {/* MARKDOWN MESSAGE */}
//                   <div className="prose prose-sm max-w-none whitespace-pre-wrap break-words">
//                     <ReactMarkdown>
//                       {msg.text}
//                     </ReactMarkdown>
//                   </div>

//                   {/* SOURCES / CITATIONS */}
//                   {msg.sender === "bot" &&
//                     msg.sources &&
//                     msg.sources.length > 0 && (
//                       <div
//                         className={`mt-3 pt-3 border-t text-xs space-y-1 ${
//                           darkMode
//                             ? "border-gray-700 text-gray-300"
//                             : "border-gray-200 text-gray-500"
//                         }`}
//                       >
//                         <p className="font-semibold">
//                           Sources / Citations
//                         </p>

//                         {msg.sources.map((source, sourceIndex) => (
//                           <p key={sourceIndex}>
//                             Page:{" "}
//                             {source.page ||
//                               source.page_number ||
//                               "N/A"}{" "}
//                             {source.label
//                               ? `• ${source.label}`
//                               : ""}
//                           </p>
//                         ))}
//                       </div>
//                     )}

//                   {/* TIME + COPY */}
//                   <div
//                     className={`flex items-center gap-3 mt-2 text-[10px] opacity-70 ${
//                       msg.sender === "user"
//                         ? "justify-end"
//                         : "justify-between"
//                     }`}
//                   >
//                     <span>{msg.time}</span>

//                     {msg.sender === "bot" && (
//                       <button
//                         onClick={() =>
//                           handleCopy(msg.text, index)
//                         }
//                         className={`text-[11px] hover:underline ${
//                           darkMode
//                             ? "text-blue-300"
//                             : "text-blue-600"
//                         }`}
//                       >
//                         {copiedIndex === index
//                           ? "Copied"
//                           : "Copy"}
//                       </button>
//                     )}
//                   </div>
//                 </div>
//               </div>
//             ))}

//             {/* SUGGESTED QUESTIONS */}
//             {messages.length === 1 && !loading && (
//               <div className="flex flex-wrap gap-2 mt-2">
//                 {suggestedQuestions.map((question, index) => (
//                   <button
//                     key={index}
//                     onClick={() => setInput(question)}
//                     className={`border px-3 py-2 rounded-full text-sm ${
//                       darkMode
//                         ? "bg-gray-800 border-gray-700 text-gray-100 hover:bg-gray-700"
//                         : "bg-white border-gray-300 text-gray-700 hover:bg-gray-100"
//                     }`}
//                   >
//                     {question}
//                   </button>
//                 ))}
//               </div>
//             )}

//             {/* TYPING DOTS */}
//             {loading && (
//               <div className="flex justify-start">
//                 <div
//                   className={`border rounded-xl px-4 py-3 shadow-sm ${
//                     darkMode
//                       ? "bg-gray-800 border-gray-700"
//                       : "bg-white border-gray-200"
//                   }`}
//                 >
//                   <div className="flex space-x-1">
//                     <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
//                     <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></div>
//                     <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></div>
//                   </div>
//                 </div>
//               </div>
//             )}

//             <div ref={messagesEndRef} />
//           </div>

//           {/* INPUT AREA */}
//           <div
//             className={`p-3 border-t ${
//               darkMode
//                 ? "bg-gray-900 border-gray-700"
//                 : "bg-white border-gray-200"
//             }`}
//           >
//             <div className="flex items-end gap-2">
//               <textarea
//                 className={`flex-1 border rounded-lg px-3 py-2 outline-none resize-none min-h-[38px] max-h-24 overflow-y-auto ${
//                   darkMode
//                     ? "bg-gray-800 text-white border-gray-600"
//                     : "bg-white text-gray-900 border-gray-300"
//                 }`}
//                 placeholder="Ask about contract..."
//                 value={input}
//                 onChange={(e) => setInput(e.target.value)}
//                 rows={1}
//                 disabled={loading}
//                 onInput={(e) => {
//                   e.target.style.height = "auto";
//                   e.target.style.height =
//                     Math.min(e.target.scrollHeight, 96) + "px";
//                 }}
//                 onKeyDown={(e) => {
//                   if (e.key === "Enter" && !e.shiftKey) {
//                     e.preventDefault();
//                     handleSend();
//                   }
//                 }}
//               />

//               <button
//                 onClick={handleSend}
//                 disabled={loading}
//                 className={`text-white px-5 py-2 rounded-lg flex items-center justify-center h-[38px] ${
//                   loading
//                     ? "bg-gray-400 cursor-not-allowed"
//                     : "bg-blue-600 hover:bg-blue-700"
//                 }`}
//               >
//                 {loading ? "..." : "Send"}
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
//     </Layout>
//   );
// }

// export default Chatbot;










//changes 


import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import Layout from "../components/layout/Layout";
import {
  chatWithContract,
  getContracts,
} from "../services/api";
import {
  Bot,
  User,
  Send,
  Copy,
  Check,
  FileText,
  Sparkles,
  Trash2,
} from "lucide-react";

function Chatbot() {
  const getTime = () =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I am your AI contract assistant. Select a contract and ask me anything about clauses, risks, payments, termination, or confidentiality.",
      time: getTime(),
      sources: [],
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [contracts, setContracts] = useState([]);
  const [selectedContractId, setSelectedContractId] = useState("");
  const [copiedIndex, setCopiedIndex] = useState(null);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  useEffect(() => {
    const fetchContracts = async () => {
      try {
        const data = await getContracts();
        setContracts(data || []);

        if (data && data.length > 0) {
          setSelectedContractId(data[0].contract_id);
        }
      } catch (error) {
        console.log("Contracts fetch error:", error);
      }
    };

    fetchContracts();
  }, []);

  const handleCopy = async (text, index) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIndex(index);

      setTimeout(() => {
        setCopiedIndex(null);
      }, 1500);
    } catch (error) {
      console.log("Copy failed:", error);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        sender: "bot",
        text: "Chat cleared. Ask me a new question about your contract.",
        time: getTime(),
        sources: [],
      },
    ]);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    if (!selectedContractId) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Please select a contract first.",
          time: getTime(),
          sources: [],
        },
      ]);
      return;
    }

    const question = input;

    const userMessage = {
      sender: "user",
      text: question,
      time: getTime(),
      sources: [],
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const data = await chatWithContract(
        selectedContractId,
        question
      );

      const botMessage = {
        sender: "bot",
        text:
          data.answer ||
          data.response ||
          data.message ||
          "No response received.",
        time: getTime(),
        sources:
          data.sources ||
          data.citations ||
          data.context ||
          [],
      };

      setMessages((prev) => [...prev, botMessage]);
   } catch (error) {
  console.log("Chat error:", error);

  setMessages((prev) => [
    ...prev,
    {
      sender: "bot",
      text:
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Backend unavailable. Please try again later.",
      time: getTime(),
      sources: [],
    },
  ]);
} finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "What is the termination clause?",
    "Summarize payment obligations",
    "Explain confidentiality clause",
    "What are the high risk clauses?",
  ];

  return (
    <Layout fullWidth={true}>
      <div className="flex h-[calc(100vh-80px)] bg-slate-100">
        <aside className="hidden w-80 border-r bg-white p-5 lg:block">
          <div className="rounded-3xl bg-gradient-to-br from-slate-950 via-blue-950 to-indigo-900 p-6 text-white shadow-xl">
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/10">
              <Bot size={28} />
            </div>

            <h2 className="text-2xl font-bold">
              AI Contract Chatbot
            </h2>

            <p className="mt-2 text-sm text-slate-300">
              Ask contract-aware questions using AI retrieval and legal context.
            </p>
          </div>

          <div className="mt-6 rounded-3xl border bg-slate-50 p-5">
            <h3 className="mb-3 font-bold text-slate-900">
              Selected Contract
            </h3>

            <select
              value={selectedContractId}
              onChange={(e) =>
                setSelectedContractId(e.target.value)
              }
              className="w-full rounded-xl border bg-white px-4 py-3 text-sm outline-none focus:border-blue-500"
            >
              <option value="">Choose contract</option>

              {contracts.map((contract) => (
                <option
                  key={contract.contract_id}
                  value={contract.contract_id}
                >
                  {contract.filename || contract.contract_id}
                </option>
              ))}
            </select>
          </div>

          <div className="mt-6 rounded-3xl border bg-white p-5">
            <h3 className="mb-4 font-bold text-slate-900">
              Suggested Prompts
            </h3>

            <div className="space-y-3">
              {suggestedQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => setInput(question)}
                  className="w-full rounded-2xl bg-slate-50 px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-blue-50 hover:text-blue-700"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleClearChat}
            className="mt-6 flex w-full items-center justify-center gap-2 rounded-2xl bg-red-50 px-4 py-3 font-semibold text-red-600 transition hover:bg-red-100"
          >
            <Trash2 size={18} />
            Clear Chat
          </button>
        </aside>

        <main className="flex flex-1 flex-col">
          <header className="flex items-center justify-between border-b bg-white px-6 py-4">
            <div>
              <div className="mb-1 inline-flex items-center gap-2 rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-600">
                <Sparkles size={14} />
                Contract-aware AI assistant
              </div>

              <h1 className="text-2xl font-bold text-slate-900">
                Contract Chatbot
              </h1>
            </div>

            <div className="flex items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3">
              <FileText size={18} className="text-blue-600" />
              <span className="text-sm font-semibold text-slate-700">
                {contracts.find(
                  (c) => c.contract_id === selectedContractId
                )?.filename || "No contract selected"}
              </span>
            </div>
          </header>

          <section className="flex-1 overflow-y-auto px-6 py-6">
            <div className="mx-auto max-w-5xl space-y-5">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex gap-3 ${
                    msg.sender === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  {msg.sender === "bot" && (
                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-blue-600 text-white">
                      <Bot size={22} />
                    </div>
                  )}

                  <div
                    className={`max-w-3xl rounded-3xl px-5 py-4 shadow-sm ${
                      msg.sender === "user"
                        ? "bg-blue-600 text-white"
                        : "border bg-white text-slate-800"
                    }`}
                  >
                    <div className="prose prose-sm max-w-none whitespace-pre-wrap break-words">
                      <ReactMarkdown>
                        {msg.text}
                      </ReactMarkdown>
                    </div>

                    {msg.sender === "bot" &&
                      msg.sources &&
                      msg.sources.length > 0 && (
                        <div className="mt-4 rounded-2xl bg-slate-50 p-3 text-xs text-slate-600">
                          <p className="mb-2 font-bold">
                            Sources / Citations
                          </p>

                          {msg.sources.map((source, sourceIndex) => (
                            <p key={sourceIndex}>
                              Page:{" "}
                              {source.page ||
                                source.page_number ||
                                "N/A"}{" "}
                              {source.label
                                ? `• ${source.label}`
                                : ""}
                            </p>
                          ))}
                        </div>
                      )}

                    <div
                      className={`mt-3 flex items-center gap-3 text-xs ${
                        msg.sender === "user"
                          ? "justify-end text-blue-100"
                          : "justify-between text-slate-400"
                      }`}
                    >
                      <span>{msg.time}</span>

                      {msg.sender === "bot" && (
                        <button
                          onClick={() =>
                            handleCopy(msg.text, index)
                          }
                          className="flex items-center gap-1 text-blue-600 hover:underline"
                        >
                          {copiedIndex === index ? (
                            <>
                              <Check size={14} />
                              Copied
                            </>
                          ) : (
                            <>
                              <Copy size={14} />
                              Copy
                            </>
                          )}
                        </button>
                      )}
                    </div>
                  </div>

                  {msg.sender === "user" && (
                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-slate-900 text-white">
                      <User size={22} />
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="flex justify-start gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-600 text-white">
                    <Bot size={22} />
                  </div>

                  <div className="rounded-3xl border bg-white px-5 py-4 shadow-sm">
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400"></span>
                      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:0.2s]"></span>
                      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:0.4s]"></span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </section>

          <footer className="border-t bg-white p-4">
            <div className="mx-auto flex max-w-5xl items-end gap-3 rounded-3xl border bg-slate-50 p-3">
              <textarea
                className="max-h-32 min-h-[48px] flex-1 resize-none bg-transparent px-3 py-3 outline-none"
                placeholder="Ask about termination, confidentiality, payment terms..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={1}
                disabled={loading}
                onInput={(e) => {
                  e.target.style.height = "auto";
                  e.target.style.height =
                    Math.min(e.target.scrollHeight, 128) + "px";
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
                disabled={loading}
                className={`flex h-12 w-12 items-center justify-center rounded-2xl text-white transition ${
                  loading
                    ? "bg-slate-400"
                    : "bg-blue-600 hover:bg-blue-700"
                }`}
              >
                <Send size={20} />
              </button>
            </div>
          </footer>
        </main>
      </div>
    </Layout>
  );
}

export default Chatbot;