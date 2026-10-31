import { useState } from "react";
import { STATUS_LABELS, type Issue, type IssueStatus } from "../lib/issues";
import { getDepartment } from "../lib/departments";
import { formatTimeAgo } from "../lib/format";

export function StatusBadge({ status }: { status: IssueStatus }) {
  return <span className={`badge badge-${status}`}>{STATUS_LABELS[status]}</span>;
}

interface IssueCardProps {
  issue: Issue;
  featured?: boolean;
  delayMs?: number;
}

const EXCERPT_THRESHOLD = 160;

export function IssueCard({ issue, featured = false, delayMs = 0 }: IssueCardProps) {
  const [expanded, setExpanded] = useState(false);
  const department = getDepartment(issue.department);
  const isLong = issue.description.length > EXCERPT_THRESHOLD;

  return (
    <article
      className={`issue-card${featured ? " featured" : ""}`}
      style={{ animationDelay: `${delayMs}ms` }}
    >
      <div className="issue-photo">
        <img src={issue.photo_url} alt={department.name} loading="lazy" />
        <span className="badge badge-dept">{issue.department}</span>
        {issue.priority === "urgent" && <span className="badge badge-urgent">Urgent</span>}
      </div>
      <div className="issue-body">
        <div className="issue-meta">
          <StatusBadge status={issue.status} />
          <span>{formatTimeAgo(issue.created_at)}</span>
        </div>
        <h3 className="issue-title">{issue.title}</h3>
        <p className="issue-address">{issue.address}</p>
        <p className={`issue-excerpt${isLong && !expanded ? " clamped" : ""}`}>{issue.description}</p>
        {isLong && (
          <button type="button" className="link-button" onClick={() => setExpanded((v) => !v)}>
            {expanded ? "Show less" : "Read more"}
          </button>
        )}
      </div>
    </article>
  );
}
