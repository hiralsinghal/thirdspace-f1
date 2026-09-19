import Link from "next/link";

export default function Navbar() {
    return (
        <nav className="flex justify-center items-center text-center p-5 gap-4 backdrop-blur-sm bg-[#ff1e00cc] w-4xs mx-auto mt-5 rounded-2xl font-body">
            <Link href="/">Home</Link>
            <Link href="drivers">Drivers</Link>
            <Link href="/teams">Teams</Link>
            <Link href="/replay">Replay</Link>
            <Link href="/strategy">Strategy</Link>
        </nav>
    );
}