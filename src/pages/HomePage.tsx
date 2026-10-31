import { Link } from "react-router-dom";
import { IssueFeed } from "../components/IssueFeed";

export function HomePage() {
  return (
    <>
      <section className="hero">
        <div className="container">
          <div className="hero-inner">
            <span className="eyebrow">Civic reporting, made human</span>
            <h1 className="hero-quote">Small voices. Big changes.</h1>
            <p className="hero-sub">
              Spotted a problem in your neighborhood? Tell us where it is and we will send it straight to the
              city team that can fix it. Follow every update from here.
            </p>
            <div className="hero-actions">
              <Link to="/report" className="btn btn-primary">
                Report an issue
              </Link>
              <a href="#updates" className="btn btn-secondary">
                See recent updates
              </a>
            </div>
          </div>
        </div>
      </section>

      <section id="updates" className="feed-section">
        <div className="container">
          <IssueFeed />
        </div>
      </section>
    </>
  );
}
