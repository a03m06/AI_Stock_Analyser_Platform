import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
    return (
        <header className="site-navbar">
            <div className="site-navbar-inner">
                <Link to="/" className="site-navbar-title">
                    AI Stock Analyser Platform
                </Link>
            </div>
        </header>
    );
}
