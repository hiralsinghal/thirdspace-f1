"use client"
import { usePathname } from "next/navigation";
import Link from "next/link";

const NavLinks = [
    { name: "Home", path: "/"},
    { name: "Drivers", path: "/drivers"},
    { name: "Teams", path: "/teams"},
    { name: "Past Races", path: "/pastraces"},
    { name: "Replay", path: "/replay"},
    { name: "Strategy", path: "/strategy"}
]

export default function Navbar() {
    const pathname = usePathname();
    const isActive = (path: string) => path === pathname;

    return (
        <nav className="flex justify-center items-center text-center p-5 gap-4 backdrop-blur-sm bg-[#ff1e00cc] w-fit mx-auto mt-5 rounded-2xl font-body">
            {NavLinks.map((link) => {
                return (
                    <Link key={link.name} href={link.path} className={isActive(link.path) ? "" : ""}>{link.name}</Link>
                )
            })}
        </nav>
    );
}