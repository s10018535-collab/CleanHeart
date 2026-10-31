import { useEffect, useMemo, useState } from "react";
import { fetchIssues, type Issue } from "../lib/issues";
import { DEPARTMENT_NAMES, type DepartmentName } from "../lib/departments";
import { IssueCard } from "./IssueCard";

type Filter = DepartmentName | "All";
type Sort = "newest" | "urgent";

export function IssueFeed() {
  const [issues, setIssues] = useState<Issue[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [filter, setFilter] = useState<Filter>("All");
  const [sort, setSort] = useState<Sort>("newest");

  useEffect(() => {
    let active = true;
    fetchIssues()
      .then((data) => {
        if (active) {
          setError(null);
          setIssues(data);
        }
      })
      .catch((err: Error) => {
        if (active) setError(err.message);
      });
    return () => {
      active = false;
    };
  }, [reloadKey]);

  const visible = useMemo(() => {
    if (!issues) return [];
    const filtered = filter === "All" ? issues : issues.filter((i) => i.department === filter);
    if (sort === "urgent") {
      return [...filtered].sort((a, b) => {
        if (a.priority !== b.priority) return a.priority === "urgent" ? -1 : 1;
        return b.created_at.localeCompare(a.created_at);
      });
    }
    return filtered;
  }, [issues, filter, sort]);

  return (
    <div>
      <div className="section-head">
        <div>
          <h2>Latest from the community</h2>
          <p>Real reports from neighbors, with their current status.</p>
        </div>
      </div>

      <div className="toolbar">
        <div className="chips" role="group" aria-label="Filter by department">
          {(["All", ...DEPARTMENT_NAMES] as Filter[]).map((name) => (
            <button
              key={name}
              type="button"
              className={`chip${filter === name ? " active" : ""}`}
              onClick={() => setFilter(name)}
            >
              {name}
            </button>
          ))}
        </div>
        <label className="sr-only" htmlFor="feed-sort">
          Sort posts
        </label>
        <select
          id="feed-sort"
          className="select"
          value={sort}
          onChange={(e) => setSort(e.target.value as Sort)}
        >
          <option value="newest">Newest first</option>
          <option value="urgent">Urgent first</option>
        </select>
      </div>

      {error && (
        <div className="state-message error" role="alert">
          <p>{error}</p>
          <button type="button" className="btn btn-secondary btn-small" style={{ marginTop: 16 }} onClick={() => setReloadKey((k) => k + 1)}>
            Try again
          </button>
        </div>
      )}

      {!error && issues === null && (
        <div className="state-message" aria-live="polite">
          <div className="spinner" />
        </div>
      )}

      {!error && issues !== null && visible.length === 0 && (
        <div className="state-message">
          <p>No posts in this department yet. Be the first to report an issue.</p>
        </div>
      )}

      {!error && visible.length > 0 && (
        <div className="news-grid">
          {visible.map((issue, index) => (
            <IssueCard
              key={issue.id}
              issue={issue}
              featured={index === 0 && filter === "All" && sort === "newest"}
              delayMs={Math.min(index, 8) * 80}
            />
          ))}
        </div>
      )}
    </div>
  );
}
