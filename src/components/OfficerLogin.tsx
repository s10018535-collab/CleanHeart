import { useState, type FormEvent } from "react";
import { DEPARTMENT_NAMES } from "../lib/departments";
import { callOfficerApi, saveOfficerSession, type OfficerSession } from "../lib/officerApi";

export function OfficerLogin({ onSignedIn }: { onSignedIn: (session: OfficerSession) => void }) {
  const [password, setPassword] = useState("");
  const [department, setDepartment] = useState<string>(DEPARTMENT_NAMES[0]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const result = await callOfficerApi<OfficerSession>("login", { password, department });
      const session = { token: result.token, department: result.department };
      saveOfficerSession(session);
      onSignedIn(session);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign in failed. Please try again.");
    } finally {
      setSubmitting(false);
      setPassword("");
    }
  }

  return (
    <div className="panel page-narrow">
      <h2 className="panel-title">Officer sign in</h2>
      <p className="page-lead panel-lead">
        This area is for authorised city officials only. Choose your department and enter the officer password.
      </p>
      <form className="form" onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="officer-department">Your department</label>
          <select
            id="officer-department"
            className="select"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
          >
            {DEPARTMENT_NAMES.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="officer-password">Officer password</label>
          <input
            id="officer-password"
            className="input"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && (
          <div className="alert alert-error" role="alert">
            {error}
          </div>
        )}
        <button type="submit" className="btn btn-primary" disabled={submitting || password.length === 0}>
          {submitting ? "Signing in..." : "Sign in"}
        </button>
      </form>
    </div>
  );
}
