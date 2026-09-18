import Link from "next/link";

export default function Navbar() {
    return (
        <nav className="flex justify-center items-center text-center p-5 gap-4 backdrop-blur-sm bg-[#ff1e00cc] w-3xs mx-auto">
            <Link href="/">Home</Link>
            <Link href="/replay">Replay</Link>
            <Link href="/strategy">Strategy</Link>
        </nav>
    );
}