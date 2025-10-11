import React from "react";
import "./Button.css";

export interface ButtonProps {
  label: string;
  primary?: boolean;
  size?: "small" | "medium" | "large";
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  primary = false,
  size = "medium",
  onClick,
}) => {
  const variant = primary ? "primary" : "default";
  return (
    <button
      type="button"
      className={`btn btn-${size} btn-${variant}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};
