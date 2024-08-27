
import Link from 'next/link'

export default function Home() {
	return (
		<div>
			<h1>Home</h1>
			{/* Add Signin and Login Links */}
			<Link href="/auth/login">
				Login
			</Link>
			<br />
			<Link href="/auth/register">
				Signup
			</Link>
		</div>
	)
}
