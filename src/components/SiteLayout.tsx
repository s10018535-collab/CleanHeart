import { Link, NavLink } from "react-router-dom";

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="container">
        <Link to="/" className="brand" aria-label="CLEAN HEARTS home">
          <svg className="brand-heart" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 21s-7.5-4.6-9.6-9.1C.9 8.6 2.6 5 6.3 5c2 0 3.4 1.1 4.2 2.4C11.3 6.1 12.7 5 14.7 5c3.7 0 5.4 3.6 3.9 6.9C19.5 16.4 12 21 12 21z" />
          </svg>
          CLEAN HEARTS
        </Link>
        <nav className="nav-links" aria-label="Main navigation">
          <NavLink to="/" end className="nav-link">
            Updates
          </NavLink>
          <NavLink to="/report" className="nav-link">
            Report an issue
          </NavLink>
          <NavLink to="/officer" className="nav-link">
            Officer portal
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="container">
        <span>CLEAN HEARTS - Small voices. Big changes.</span>
        <span>Every report is read and routed to the team that can act on it.</span>
      </div>
    </footer>
  );
}
