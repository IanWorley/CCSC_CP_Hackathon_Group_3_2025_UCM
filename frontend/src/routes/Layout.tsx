import PWABadge from "@/PWABadge";
import { Outlet } from "react-router";

function Layout() {
    return (
        <>
            <PWABadge />
            <header className="flex items-center justify-center h-20 bg-ucm-red">
                <h1 className="text-4xl font-bold text-white">WashUCM</h1>
            </header>
            <Outlet />
        </>
    );
}

export default Layout;