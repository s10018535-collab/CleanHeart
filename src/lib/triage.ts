import { DEPARTMENTS, type DepartmentName } from "./departments";

export type Priority = "normal" | "urgent";

export interface TriageResult {
  department: DepartmentName;
  priority: Priority;
}

const URGENT_KEYWORDS = [
  "flood",
  "burst",
  "gas leak",
  "fire",
  "smoke",
  "spark",
  "exposed wire",
  "electrocut",
  "injur",
  "collaps",
  "sinkhole",
  "emergency",
  "hazard",
  "accident",
  "danger",
];

export function triageReport(text: string): TriageResult {
  const normalized = text.toLowerCase();

  let department: DepartmentName = "General Services";
  let bestScore = 0;
  for (const dept of DEPARTMENTS) {
    const score = dept.keywords.filter((keyword) => normalized.includes(keyword)).length;
    if (score > bestScore) {
      bestScore = score;
      department = dept.name;
    }
  }

  const priority: Priority = URGENT_KEYWORDS.some((keyword) => normalized.includes(keyword))
    ? "urgent"
    : "normal";

  return { department, priority };
}
