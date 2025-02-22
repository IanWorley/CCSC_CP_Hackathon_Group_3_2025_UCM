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
      <Outlet />
    </React.Fragment>
  );
}
