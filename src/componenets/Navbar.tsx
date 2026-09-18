import Link from "next/link";

export default function Navbar() {
    return (
        <nav className="flex justify-center p-4 w-sm">
            <Link href="/">Home</Link>
            <Link href="/replay">Replay</Link>
            <Link href="/strategy">Strategy</Link>
        </nav>
    );
}