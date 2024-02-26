import React from "react";

const Alert = ({ messages }) => {
  // Ensure messages is an array
  if (!Array.isArray(messages)) {
    console.warn('Alert component expects "messages" prop to be an array.');
    console.log(messages); // In Alert component
    return null; // or some fallback UI
  }

  return (
    <div>
      {messages.map((message, index) => (
        <div key={index}>{message}</div>
      ))}
    </div>
  );
};

export default Alert;