import React, { useState } from "https://esm.sh/react@18.3.1";
import { createRoot } from "https://esm.sh/react-dom@18.3.1/client";

function App() {
  const [skills, setSkills] = useState("Python, FastAPI, SQL, Machine Learning, DSA");
  const [roles, setRoles] = useState("AI Engineer, Software Engineer");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  async function runMatch() {
    setLoading(true);
    const response = await fetch("/match", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: "Candidate",
        target_roles: roles.split(",").map(x => x.trim()).filter(Boolean),
        skills: skills.split(",").map(x => x.trim()).filter(Boolean),
        years_experience: 0,
        resume_summary: "AI/ML engineering student focused on software engineering and applied machine learning."
      })
    });
    setResults(await response.json());
    setLoading(false);
  }

  return React.createElement("main", {className: "page"},
    React.createElement("section", {className: "hero"},
      React.createElement("p", {className: "eyebrow"}, "AI + SOFTWARE ENGINEERING"),
      React.createElement("h1", null, "Placement Copilot"),
      React.createElement("p", null, "Explainable job matching instead of keyword guessing.")
    ),
    React.createElement("section", {className: "panel"},
      React.createElement("label", null, "Target roles"),
      React.createElement("input", {value: roles, onChange: e => setRoles(e.target.value)}),
      React.createElement("label", null, "Skills"),
      React.createElement("input", {value: skills, onChange: e => setSkills(e.target.value)}),
      React.createElement("button", {onClick: runMatch, disabled: loading}, loading ? "Ranking…" : "Rank jobs")
    ),
    React.createElement("section", {className: "results"},
      results.map(job =>
        React.createElement("article", {className: "card", key: job.job_id},
          React.createElement("div", {className: "score"}, Math.round(job.score)),
          React.createElement("div", null,
            React.createElement("h2", null, job.title),
            React.createElement("p", null, job.company + " • " + job.location),
            React.createElement("p", null, job.reasons.join(" ")),
            job.gaps.length
              ? React.createElement("small", null, "Skill gaps: " + job.gaps.join(", "))
              : null
          )
        )
      )
    )
  );
}

createRoot(document.getElementById("root")).render(React.createElement(App));
