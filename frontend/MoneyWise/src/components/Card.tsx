import React from "react";
import "./Card.css";

interface CardProps {
  title: string;
  amount: string;
}

const Card: React.FC<CardProps> = ({ title, amount }) => {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p>{amount}</p>
    </div>
  );
};

export default Card;
