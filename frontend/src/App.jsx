import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/common/Navbar";
import Home from "./pages/Home";
import CompanyPage from "./pages/CompanyPage";

function App() {
    return (
        <BrowserRouter>
            <Navbar />

            <Routes>
                <Route
                    path="/"
                    element={<Home />}
                />

                <Route
                    path="/company/:company"
                    element={<CompanyPage />}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;