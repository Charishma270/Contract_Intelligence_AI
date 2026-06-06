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

//week 4fridayyyyyyyyyyyyy
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import Layout from "../components/layout/Layout";
import {
  chatWithContract,
  getContracts,
} from "../services/api";

function Chatbot() {
  const getTime = () =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! Ask me about your contract.",
      time: getTime(),
      sources: [],
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [contracts, setContracts] = useState([]);
  const [selectedContractId, setSelectedContractId] = useState("");
  const [darkMode, setDarkMode] = useState(false);
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
      text: input,
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

      console.log("Chat response:", data);

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

      const errorMessage = {
        sender: "bot",
        text: "Backend unavailable. Please try again later.",
        time: getTime(),
        sources: [],
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "What is the termination clause?",
    "Summarize payment obligations",
    "Explain confidentiality clause",
  ];

  return (
    <Layout fullWidth={true}>
      <div
        className={`flex flex-col h-[calc(100vh-64px)] ${
          darkMode ? "bg-gray-950 text-white" : "bg-white text-gray-900"
        }`}
      >
        {/* HEADER */}
        <div
          className={`w-full h-16 flex items-center justify-between px-6 border-b ${
            darkMode
              ? "bg-gray-900 border-gray-700"
              : "bg-white border-gray-200"
          }`}
        >
          <h2 className="text-2xl font-bold">
            Contract Chatbot
          </h2>

          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`px-4 py-2 rounded-lg text-sm font-semibold ${
              darkMode
                ? "bg-white text-gray-900"
                : "bg-gray-900 text-white"
            }`}
          >
            {darkMode ? "Light Mode" : "Dark Mode"}
          </button>
        </div>

        {/* CONTRACT SELECTOR */}
        <div
          className={`px-5 py-3 border-b ${
            darkMode
              ? "bg-gray-900 border-gray-700"
              : "bg-white border-gray-200"
          }`}
        >
          <label className="text-sm font-semibold mr-3">
            Select Contract:
          </label>

          <select
            value={selectedContractId}
            onChange={(e) =>
              setSelectedContractId(e.target.value)
            }
            className={`border rounded-lg px-3 py-2 text-sm outline-none ${
              darkMode
                ? "bg-gray-800 text-white border-gray-600"
                : "bg-white text-gray-900 border-gray-300"
            }`}
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

        {/* CHAT AREA */}
        <div
          className={`flex-1 flex flex-col ${
            darkMode ? "bg-gray-950" : "bg-white"
          }`}
        >
          <div
            className={`flex-1 overflow-y-auto p-5 space-y-4 ${
              darkMode ? "bg-gray-950" : "bg-gray-50"
            }`}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.sender === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div
                  className={`px-4 py-3 rounded-xl w-fit max-w-2xl leading-7 text-[15px] ${
                    msg.sender === "user"
                      ? "bg-blue-600 text-white"
                      : darkMode
                      ? "bg-gray-800 border border-gray-700 text-gray-100 shadow-sm max-h-[420px] overflow-y-auto"
                      : "bg-white border text-gray-800 shadow-sm max-h-[420px] overflow-y-auto"
                  }`}
                >
                  {/* MARKDOWN MESSAGE */}
                  <div className="prose prose-sm max-w-none whitespace-pre-wrap break-words">
                    <ReactMarkdown>
                      {msg.text}
                    </ReactMarkdown>
                  </div>

                  {/* SOURCES / CITATIONS */}
                  {msg.sender === "bot" &&
                    msg.sources &&
                    msg.sources.length > 0 && (
                      <div
                        className={`mt-3 pt-3 border-t text-xs space-y-1 ${
                          darkMode
                            ? "border-gray-700 text-gray-300"
                            : "border-gray-200 text-gray-500"
                        }`}
                      >
                        <p className="font-semibold">
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

                  {/* TIME + COPY */}
                  <div
                    className={`flex items-center gap-3 mt-2 text-[10px] opacity-70 ${
                      msg.sender === "user"
                        ? "justify-end"
                        : "justify-between"
                    }`}
                  >
                    <span>{msg.time}</span>

                    {msg.sender === "bot" && (
                      <button
                        onClick={() =>
                          handleCopy(msg.text, index)
                        }
                        className={`text-[11px] hover:underline ${
                          darkMode
                            ? "text-blue-300"
                            : "text-blue-600"
                        }`}
                      >
                        {copiedIndex === index
                          ? "Copied"
                          : "Copy"}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {/* SUGGESTED QUESTIONS */}
            {messages.length === 1 && !loading && (
              <div className="flex flex-wrap gap-2 mt-2">
                {suggestedQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => setInput(question)}
                    className={`border px-3 py-2 rounded-full text-sm ${
                      darkMode
                        ? "bg-gray-800 border-gray-700 text-gray-100 hover:bg-gray-700"
                        : "bg-white border-gray-300 text-gray-700 hover:bg-gray-100"
                    }`}
                  >
                    {question}
                  </button>
                ))}
              </div>
            )}

            {/* TYPING DOTS */}
            {loading && (
              <div className="flex justify-start">
                <div
                  className={`border rounded-xl px-4 py-3 shadow-sm ${
                    darkMode
                      ? "bg-gray-800 border-gray-700"
                      : "bg-white border-gray-200"
                  }`}
                >
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* INPUT AREA */}
          <div
            className={`p-3 border-t ${
              darkMode
                ? "bg-gray-900 border-gray-700"
                : "bg-white border-gray-200"
            }`}
          >
            <div className="flex items-end gap-2">
              <textarea
                className={`flex-1 border rounded-lg px-3 py-2 outline-none resize-none min-h-[38px] max-h-24 overflow-y-auto ${
                  darkMode
                    ? "bg-gray-800 text-white border-gray-600"
                    : "bg-white text-gray-900 border-gray-300"
                }`}
                placeholder="Ask about contract..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={1}
                disabled={loading}
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
                disabled={loading}
                className={`text-white px-5 py-2 rounded-lg flex items-center justify-center h-[38px] ${
                  loading
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-blue-600 hover:bg-blue-700"
                }`}
              >
                {loading ? "..." : "Send"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Chatbot;