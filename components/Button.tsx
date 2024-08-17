"use client";
import Link from "next/link";

interface ButtonProps {
  label: string;
  link: string;
}

const Button = ({ label, link }: ButtonProps) => {
  return (
    <Link href={link}>
      <button className="btn btn-block mb-6 h-20 justify-start rounded-lg bg-btn-colour text-base font-normal text-white hover:bg-btn-colour-hover">
        <div>{label}</div>
      </button>
    </Link>
  );
};

export default Button;
