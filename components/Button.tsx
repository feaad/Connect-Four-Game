import Link from "next/link";


interface ButtonProps {
    label: string;
    link: string;
}

const Button = ({ label, link }: ButtonProps) => {
  return (
    <Link href={link}>
      <button className="bg-btn-colour hover:bg-btn-colour-hover btn btn-block mb-6 h-20 justify-start rounded-lg text-base font-normal text-white">
        <div>{label}</div>
      </button>
    </Link>
  );
};

export default Button;
