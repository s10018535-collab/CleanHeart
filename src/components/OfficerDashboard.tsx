import { useEffect, useMemo, useState } from "react";
import { StatusBadge } from "./IssueCard";
import { fetchIssues, STATUS_LABELS, type Issue, type IssueStatus } from "../lib/issues";
import { callOfficerApi, OfficerApiError, type OfficerSession } from "../lib/officerApi";
import type { DepartmentName } from "../lib/departments";
import { formatTimeAgo } from "../lib/format";

const NEXT_STATUS: Record<IssueStatus, { status: IssueStatus; label: string }> = {
  new: { status: "in_progress", label: "Start work" },
  in_progress: { status: "resolved", label: "Mark resolved" },
  resolved: { status: "in_progress", label: "Reopen" },
};

const STATUS_ORDER: IssueStatus[] = ["new", "in_progress", "resolved"];

interface OfficerDashboardProps {
  session: OfficerSession;
  onSignOut: () => void;
  onSessionExpired: () => void;
}

export function OfficerDashboard({ session, onSignOut, onSessionExpired }: OfficerDashboardProps) {
  const department = session.department as DepartmentName;
  const [issues, setIssues] = useState<Issue[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<IssueStatus>("new");
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [rowError, setRowError] = useState<{ id: string; message: string } | null>(null);

  useEffect(() => {
    let active = true;
    fetchIssues(department)
      .then((data) => {
        if (active) setIssues(data);
      })
      .catch((err: Error) => {
        if (active) setLoadError(err.message);
      });
    return () => {
      active = false;
    };
  }, [department]);

  const counts = useMemo(() => {
    const result: Record<IssueStatus, number> = { new: 0, in_progress: 0, resolved: 0 };
    for (const issue of issues ?? []) result[issue.status] += 1;
    return result;
  }, [issues]);

  const visible = useMemo(
    () => (issues ?? []).filter((issue) => issue.status === statusFilter),
    [issues, statusFilter],
  );

  async function changeStatus(issue: Issue, nextStatus: IssueStatus) {
    setUpdatingId(issue.id);
    setRowError(null);
    try {
      const result = await callOfficerApi<{ id: string; status: IssueStatus }>("updateStatus", {
        token: session.token,
        issueId: issue.id,
        status: nextStatus,
      });
      setIssues((prev) =>
        (prev ?? []).map((item) => (item.id === issue.id ? { ...item, status: result.status } : item)),
      );
    } catch (err) {
      if (err instanceof OfficerApiError && err.status === 401) {
        onSessionExpired();
        return;
      }
      setRowError({ id: issue.id, message: err instanceof Error ? err.message : "Update failed." });
    } finally {
      setUpdatingId(null);
    }
  }

  return (
    <section className="page">
      <div className="container">
        <div className="dashboard-head">
          <div>
            <span className="eyebrow">Officer dashboard</span>
            <h1 className="page-title">{department}</h1>
            <p className="page-lead" style={{ marginBottom: 0 }}>
              Reports routed to your department. Update each one as work progresses.
            </p>
          </div>
          <button type="button" className="btn btn-secondary" onClick={onSignOut}>
            Sign out
          </button>
        </div>

        {loadError && (
          <div className="alert alert-error" role="alert">
            {loadError}
          </div>
        )}

        {!loadError && issues === null && (
          <div className="state-message">
            <div className="spinner" />
          </div>
        )}

        {issues !== null && (
          <>
            <div className="count-row">
              {STATUS_ORDER.map((status) => (
                <button
                  key={status}
                  type="button"
                  className={`count-card${statusFilter === status ? " active" : ""}`}
                  onClick={() => setStatusFilter(status)}
                >
                  <div className="count-value">{counts[status]}</div>
                  <div className="count-label">{STATUS_LABELS[status]}</div>
                </button>
              ))}
            </div>

            {visible.length === 0 ? (
              <div className="state-message">
                <p>No reports with this status right now.</p>
              </div>
            ) : (
              <div className="issue-list">
                {visible.map((issue) => {
                  const next = NEXT_STATUS[issue.status];
                  return (
                    <article key={issue.id} className="issue-row">
                      <div className="issue-row-main">
                        <div className="issue-meta">
                          <StatusBadge status={issue.status} />
                          {issue.priority === "urgent" && <span className="badge badge-urgent">Urgent</span>}
                          <span>{formatTimeAgo(issue.created_at)}</span>
                        </div>
                        <h3 className="issue-row-title">
                          {issue.title}
                        </h3>
                        <p className="issue-address">{issue.address}</p>
                        <p className="issue-excerpt">{issue.description}</p>
                      </div>
                      <div className="issue-row-actions">
                        <button
                          type="button"
                          className="btn btn-sage btn-small"
                          disabled={updatingId === issue.id}
                          onClick={() => changeStatus(issue, next.status)}
                        >
                          {updatingId === issue.id ? "Saving..." : next.label}
                        </button>
                        {rowError?.id === issue.id && <p className="row-error">{rowError.message}</p>}
                      </div>
                    </article>
                  );
                })}
              </div>
            )}
          </>
        )}
      </div>
    </section>
  );
}
