import { Route, Routes } from "react-router-dom";
import { SiteFooter, SiteHeader } from "./components/SiteLayout";
import { HomePage } from "./pages/HomePage";
import { ReportPage } from "./pages/ReportPage";
import { OfficerPage } from "./pages/OfficerPage";

export default function App() {
  return (
    <>
      <SiteHeader />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/report" element={<ReportPage />} />
          <Route path="/officer" element={<OfficerPage />} />
        </Routes>
      </main>
      <SiteFooter />
    </>
  );
}
