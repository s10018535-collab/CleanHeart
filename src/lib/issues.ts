import { supabase } from "./supabase";
import type { DepartmentName } from "./departments";
import type { Priority } from "./triage";

export type IssueStatus = "new" | "in_progress" | "resolved";

export interface Issue {
  id: string;
  title: string;
  description: string;
  address: string;
  department: DepartmentName;
  priority: Priority;
  status: IssueStatus;
  photo_url: string;
  created_at: string;
}

export const STATUS_LABELS: Record<IssueStatus, string> = {
  new: "New",
  in_progress: "In progress",
  resolved: "Resolved",
};

const ISSUE_COLUMNS =
  "id, title, description, address, department, priority, status, photo_url, created_at";

export async function fetchIssues(department?: DepartmentName): Promise<Issue[]> {
  let query = supabase
    .from("issues")
    .select(ISSUE_COLUMNS)
    .order("created_at", { ascending: false })
    .limit(100);

  if (department) {
    query = query.eq("department", department);
  }

  const { data, error } = await query;
  if (error) throw new Error("We could not load the posts. Please try again.");
  return (data ?? []) as Issue[];
}

export interface NewIssueInput {
  title: string;
  description: string;
  address: string;
  department: DepartmentName;
  priority: Priority;
  photo_url: string;
}

export async function createIssue(input: NewIssueInput): Promise<void> {
  const { error } = await supabase.from("issues").insert({ ...input, status: "new" });
  if (error) throw new Error("Your report could not be sent. Please check it and try again.");
}
