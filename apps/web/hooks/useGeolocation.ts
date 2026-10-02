"use client";
import { useState, useEffect } from "react";

/** Real browser geolocation — never a hardcoded fallback coordinate.
 * Returns null until the browser actually provides a position (or denies),
 * so callers must treat "no location yet" as a real state to handle
 * (disable submit / ask the user to type coordinates), not silently
 * substitute a guessed value. */
export function useGeolocation() {
  const [position, setPosition] = useState<{ latitude: number; longitude: number } | null>(null);
  const [status, setStatus] = useState<"idle" | "locating" | "granted" | "denied" | "unsupported">("idle");

  function request() {
    if (typeof navigator === "undefined" || !navigator.geolocation) {
      setStatus("unsupported");
      return;
    }
    setStatus("locating");
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setPosition({ latitude: pos.coords.latitude, longitude: pos.coords.longitude });
        setStatus("granted");
      },
      () => setStatus("denied"),
      { timeout: 8000 }
    );
  }

  return { position, status, request };
}
