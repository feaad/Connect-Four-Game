import React, { useEffect, useRef } from "react";
import { set } from "zod";
const SHAPES = ["square", "triangle", "rectangle"];
const COLOUR_DIGIT = "ABCDEF1234567890";

const Confetti = () => {
	const [isConfettiActive, setConfettiActive] = React.useState(false);
	const containerRef = useRef<HTMLDivElement>(null);

	const generateConfetti = () => {
		const container = containerRef.current;
		if (container) {
			for (let i = 0; i < 50; i++) {
				const confetti = document.createElement("div");
				const positionX = Math.random() * window.innerWidth;
				const positionY = Math.random() * window.innerHeight;
				const rotation = Math.random() * 360;
				const size = Math.floor(Math.random() * (20 - 5 + 1)) + 5; // Set confetti styles
				confetti.style.left = `${positionX}px`;
				confetti.style.top = `${positionY}px`;
				confetti.style.transform = `rotate(${rotation}deg)`;
				confetti.className =
					"confetti " + SHAPES[Math.floor(Math.random() * 3)];
				confetti.style.width = `${size}px`;
				confetti.style.height = `${size}px`;
				confetti.style.backgroundColor = generateRandomColour(); // Append confetti to the container
				container.appendChild(confetti);
				// add confetti element after animation duration (4 seconds)
				setTimeout(() => {
					// container.removeChild(confetti);
					container.appendChild(confetti);
				}, 10);
			}
		}
	};

	const handleClick = () => {
		setConfettiActive(true);
		setTimeout(() => {
			setConfettiActive(false);
		}, 4000);
	};

	useEffect(() => {
		handleClick();
		if (isConfettiActive) {
			generateConfetti();
		}
	}, [isConfettiActive]);

	return (
		<div>
			<div
				className='fixed top-0 left-0 w-full h-full pointer-events-none'
				ref={containerRef}
				id='confetti-container'
			></div>
		</div>
	);
};

const generateRandomColour = () => {
	let colour = "#";
	for (let i = 0; i < 6; i++) {
		colour += COLOUR_DIGIT[Math.floor(Math.random() * 16)];
	}
	return colour;
};
export default Confetti;
