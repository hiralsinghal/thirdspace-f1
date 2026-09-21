import Link from "next/link";
import Image from "next/image";

export default function NotFound() {
    return (
        <div className="flex flex-col items-center justify-center mx-auto text-center">
            <h1 className="font-bold text-[200px] font-heading">404</h1>
            <Image src="https://i.pinimg.com/736x/29/a7/97/29a797972ea730a4ff4b26855e6afa3f.jpg" width={400} height={250} alt="max"></Image>
            <p className="font-data">Where are you? Lost lol!</p>
            <p className="font-data"><Link href="/">Wanna go back? Here you go!</Link></p>
        </div>
    );
}