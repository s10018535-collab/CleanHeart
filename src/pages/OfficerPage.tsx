import { useEffect, useState } from "react";
import { OfficerDashboard } from "../components/OfficerDashboard";
import { OfficerLogin } from "../components/OfficerLogin";
import {
  callOfficerApi,
  clearOfficerSession,
  loadOfficerSession,
  OfficerApiError,
  type OfficerSession,
} from "../lib/officerApi";

export function OfficerPage() {
  const [session, setSession] = useState<OfficerSession | null>(() => loadOfficerSession());
  const [checking, setChecking] = useState(session !== null);

  useEffect(() => {
    if (!session) return;
    let active = true;
    callOfficerApi("session", { token: session.token })
      .catch((err: unknown) => {
        if (active && err instanceof OfficerApiError && err.status === 401) {
          clearOfficerSession();
          setSession(null);
        }
      })
      .finally(() => {
        if (active) setChecking(false);
      });
    return () => {
      active = false;
    };
  }, []);

  async function signOut() {
    if (session) {
      await callOfficerApi("logout", { token: session.token }).catch(() => undefined);
    }
    clearOfficerSession();
    setSession(null);
  }

  function handleSessionExpired() {
    clearOfficerSession();
    setSession(null);
  }

  if (checking) {
    return (
      <section className="page">
        <div className="container">
          <div className="state-message">
            <div className="spinner" />
          </div>
        </div>
      </section>
    );
  }

  if (!session) {
    return (
      <section className="page">
        <div className="container">
          <OfficerLogin onSignedIn={setSession} />
        </div>
      </section>
    );
  }

  return (
    <OfficerDashboard session={session} onSignOut={signOut} onSessionExpired={handleSessionExpired} />
  );
}
