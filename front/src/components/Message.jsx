import React from "react";
import "./Message.css";

const Message = ({ content, sender }) => {
  return (
    <div className={`message ${sender}`}>
      <p>{content}</p>
    </div>
  );
};

export default Message;
