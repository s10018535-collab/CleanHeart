export const DEPARTMENT_NAMES = [
  "Public Works",
  "Water & Drainage",
  "Sanitation",
  "Electrical & Lighting",
  "Parks & Recreation",
  "Public Safety",
  "General Services",
] as const;

export type DepartmentName = (typeof DEPARTMENT_NAMES)[number];

export interface Department {
  name: DepartmentName;
  summary: string;
  photo: string;
  keywords: readonly string[];
}

export const DEPARTMENTS: readonly Department[] = [
  {
    name: "Public Works",
    summary: "Roads, potholes, sidewalks and traffic signs",
    photo: "https://images.pexels.com/photos/6018646/pexels-photo-6018646.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    keywords: ["pothole", "road", "asphalt", "sidewalk", "pavement", "crack", "bridge", "speed bump", "manhole", "curb"],
  },
  {
    name: "Water & Drainage",
    summary: "Leaks, burst pipes, sewers and flooding",
    photo: "https://images.pexels.com/photos/28447789/pexels-photo-28447789.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    keywords: ["water", "leak", "pipe", "drain", "sewer", "flood", "puddle", "main", "sink hole", "wet"],
  },
  {
    name: "Sanitation",
    summary: "Rubbish, bins, litter and bad smells",
    photo: "https://images.pexels.com/photos/4651148/pexels-photo-4651148.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    keywords: ["garbage", "trash", "rubbish", "bin", "waste", "dump", "litter", "smell", "rat", "recycl"],
  },
  {
    name: "Electrical & Lighting",
    summary: "Streetlights, power lines and outages",
    photo: "https://images.pexels.com/photos/9971141/pexels-photo-9971141.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    keywords: ["streetlight", "street light", "light", "lamp", "power", "electric", "wire", "outage", "pole", "dark"],
  },
  {
    name: "Parks & Recreation",
    summary: "Playgrounds, benches, trees and green spaces",
    photo: "https://images.pexels.com/photos/32801503/pexels-photo-32801503.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    keywords: ["park", "playground", "swing", "slide", "bench", "tree", "grass", "garden", "trail", "overgrown"],
  },
  {
    name: "Public Safety",
    summary: "Crosswalks, traffic signals and unsafe areas",
    photo: "https://images.pexels.com/photos/10121600/pexels-photo-10121600.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    keywords: ["crosswalk", "signal", "traffic light", "stop sign", "unsafe", "safety", "crime", "speeding", "vandal", "fight"],
  },
  {
    name: "General Services",
    summary: "Anything else that needs a city team",
    photo: "https://images.pexels.com/photos/11733144/pexels-photo-11733144.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    keywords: [],
  },
];

export function getDepartment(name: string): Department {
  return DEPARTMENTS.find((d) => d.name === name) ?? DEPARTMENTS[DEPARTMENTS.length - 1];
}
