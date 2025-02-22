import { Outlet, createRootRoute } from "@tanstack/react-router";
import * as React from "react";
import PWABadge from "../PWABadge";

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  return (
    <React.Fragment>
      <PWABadge />
      <header className="flex items-center justify-center h-20 bg-ucm_red">
        <h1 className="text-4xl font-bold text-white">WashUCM</h1>
      </header>
      <Outlet />
    </React.Fragment>
  );
}
