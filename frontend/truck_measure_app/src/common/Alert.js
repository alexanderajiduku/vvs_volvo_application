import React from "react";

const Alert = ({ messages }) => {
  if (!Array.isArray(messages)) {
    return null; 
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