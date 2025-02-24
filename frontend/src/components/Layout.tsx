import { Outlet } from "react-router"
import PWABadge from '../PWABadge.tsx'

function Layout() {
    return (
        <>
            <header className="flex items-center justify-center h-20 bg-ucm-red">
                <h1 className="text-4xl font-bold text-white">WashUCM</h1>
            </header>
            <main>
                <Outlet />
            </main>
            <PWABadge />
        </>
    )
}

export default Layout