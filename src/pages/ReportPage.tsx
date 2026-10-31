import { useMemo, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { createIssue } from "../lib/issues";
import { getDepartment } from "../lib/departments";
import { triageReport } from "../lib/triage";

const LIMITS = {
  title: { min: 3, max: 120 },
  description: { min: 10, max: 2000 },
  address: { min: 5, max: 200 },
};

interface ReportValues {
  title: string;
  description: string;
  address: string;
}

const EMPTY_VALUES: ReportValues = { title: "", description: "", address: "" };

function validate(values: ReportValues): string | null {
  if (values.title.length < LIMITS.title.min) return `Please give the issue a short title (at least ${LIMITS.title.min} characters).`;
  if (values.description.length < LIMITS.description.min) return `Please describe the problem in a little more detail (at least ${LIMITS.description.min} characters).`;
  if (values.address.length < LIMITS.address.min) return "Please add the street address or nearest landmark.";
  return null;
}

export function ReportForm({ onSubmitted }: { onSubmitted: (departmentName: string) => void }) {
  const [values, setValues] = useState<ReportValues>(EMPTY_VALUES);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const triage = useMemo(
    () => triageReport(`${values.title} ${values.description}`),
    [values.title, values.description],
  );
  const hasText = values.title.trim().length > 0 || values.description.trim().length > 0;

  function updateField(field: keyof ReportValues, value: string) {
    setValues((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const cleaned: ReportValues = {
      title: values.title.trim(),
      description: values.description.trim(),
      address: values.address.trim(),
    };
    const problem = validate(cleaned);
    if (problem) {
      setError(problem);
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await createIssue({
        ...cleaned,
        department: triage.department,
        priority: triage.priority,
        photo_url: getDepartment(triage.department).photo,
      });
      onSubmitted(triage.department);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Your report could not be sent.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="form" onSubmit={handleSubmit} noValidate>
      <div className="field">
        <label htmlFor="report-title">What is the problem?</label>
        <input
          id="report-title"
          className="input"
          maxLength={LIMITS.title.max}
          placeholder="e.g. Deep pothole on Maple Avenue"
          value={values.title}
          onChange={(e) => updateField("title", e.target.value)}
        />
      </div>

      <div className="field">
        <label htmlFor="report-description">Tell us more</label>
        <textarea
          id="report-description"
          className="textarea"
          maxLength={LIMITS.description.max}
          placeholder="What is happening, how long has it been there, and who it affects?"
          value={values.description}
          onChange={(e) => updateField("description", e.target.value)}
        />
        <span className="field-hint">
          {values.description.length} / {LIMITS.description.max} characters
        </span>
      </div>

      <div className="field">
        <label htmlFor="report-address">Where is it?</label>
        <input
          id="report-address"
          className="input"
          maxLength={LIMITS.address.max}
          placeholder="Street address or nearest landmark"
          value={values.address}
          onChange={(e) => updateField("address", e.target.value)}
        />
      </div>

      {hasText ? (
        <div className="triage-card" aria-live="polite">
          <span>
            This will be sent to <strong>{triage.department}</strong>
          </span>
          {triage.priority === "urgent" ? (
            <span className="badge badge-urgent">Marked urgent</span>
          ) : (
            <span className="badge badge-dept">Standard priority</span>
          )}
        </div>
      ) : (
        <p className="field-hint">We will automatically send your report to the right city team.</p>
      )}

      {error && (
        <div className="alert alert-error" role="alert">
          {error}
        </div>
      )}

      <div className="form-actions">
        <Link to="/" className="btn btn-secondary">
          Cancel
        </Link>
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? "Sending..." : "Send report"}
        </button>
      </div>
    </form>
  );
}

export function ReportPage() {
  const [routedTo, setRoutedTo] = useState<string | null>(null);

  return (
    <section className="page">
      <div className="container">
        <div className="page-narrow">
          <span className="eyebrow">Report an issue</span>
          <h1 className="page-title">Tell us what needs fixing</h1>
          <p className="page-lead">
            Describe the problem and where it is. Your report goes straight to the team responsible for it, and
            it appears on the updates page for neighbors to see.
          </p>

          <div className="panel">
            {routedTo ? (
              <div className="success-panel">
                <div className="success-icon" aria-hidden="true">
                  ✓
                </div>
                <h2>Thank you, your voice matters</h2>
                <p className="page-lead success-text">
                  Your report has been sent to <strong>{routedTo}</strong>. It is now visible to the community.
                </p>
                <div className="form-actions success-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setRoutedTo(null)}>
                    Report another issue
                  </button>
                  <Link to="/" className="btn btn-primary">
                    View updates
                  </Link>
                </div>
              </div>
            ) : (
              <ReportForm onSubmitted={setRoutedTo} />
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
