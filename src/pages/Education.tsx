import { useState } from "react";
import Section from "../components/Section";
import Button from "../components/Button";
import Modal from "../components/Modal";

interface Course {
  title: string;
  institution: string;
  year: string;

  hours?: string;
  country?: string;

  type?: "course" | "certification";
  mode?: "online" | "presential" | "hybrid";
  level?: "basic" | "intermediate" | "advanced";

  skills?: string[];
  description?: string;
  credentialUrl?: string;
}
interface Event {
  title: string;
  hours: string;
}

interface Academic {
  title: string;
}

const EVENTS: Event[] = [
  { title: "SNCT Lecture 2019: Sustainable Stingless Beekeeping (ASF)", hours: "6h" },
  { title: "SNCT Catarinense 2021 – Thematic Table with external extensionist entities and students", hours: "3h" },
  { title: "Co-designing application-specific quantum accelerators for HPC", hours: "1h" },
  { title: "7º Teaching, Research, Extension and Innovation Seminar IFSC (SEPEI 2018)", hours: "27h" },
  { title: "Lecture: 5G and IoT Connectivity", hours: "2h" },
  { title: "Progress in Photonic Quantum Computing", hours: "1h" },
  { title: "Minicourse: Introduction to quantum information using Qiskit", hours: "4h" },
];


/*
Cyber Attacks

Cybersecurity Processes

Cybersecurity Risk Management

Cyber Threat Analysis

Cyber Threat Intelligence

Incident Response

Information Security

PWID-B0454800

Security Strategies

Social Engineering

Threat Analysis
*/
const COURSES: Course[] = [
  {
    title: "Cybersecurity Fundamentals",
    institution: "IBM",
    year: "2020",
    type: "certification",
    mode: "online",
    level: "basic",
    hours: "N/A",
    skills: ["Cybersecurity", "Cryptography", "Compliance", "Vulnerability Management", "Threat Detection"],
    description:
      "Introduction to cybersecurity concepts, risk management, cryptography fundamentals and enterprise security practices.",
    credentialUrl: "https://www.credly.com/badges/d0ca5898-8890-49e0-ae9e-59efec9dd764"
  }, 
  {
    title: "Student Journey Blockchain Training",
    hours: "4h",
    institution: "Universidade Federal de Santa Catarina (UFSC)",
    country: "Brazil",
    year: "2023",
    type: "course",
    skills: ["Blockchain fundamentals"],
  },
  {
    title: "Configuration of Linux Computer Networks",
    hours: "60h",
    institution: "IFSC - Santa Catarina - SC",
    country: "Brazil",
    year: "2021",
    skills: ["Linux", "Computer Networks"],
  },
  {
    title: "Front-End Programming",
    hours: "40h",
    institution: "IFSC - Santa Catarina - SC",
    country: "Brazil",
    year: "2021",
    skills: ["HTML5", "CSS", "Angular", "JavaScript"],
  },
  {
    title: "Back-End Programming",
    hours: "60h",
    institution: "IFSC - Instituto Federal de Santa Catarina",
    country: "Brazil",
    year: "2021",
    skills: [".NET Framework", "AWS", "JavaScript"],
  },
  {
    title: "Fundamentals of Programming",
    hours: "60h",
    institution: "IFSC - Instituto Federal de Santa Catarina",
    country: "Brazil",
    year: "2021",
    skills: ["TypeScript", "JavaScript"],
  },
  {
    title: "Database",
    hours: "40h",
    institution: "IFSC - Instituto Federal de Santa Catarina",
    country: "Brazil",
    year: "2021",
    skills: ["SQL", "MySQL", "ProgreSQL", "MongoDB"],
  },
  {
    title: "Object Oriented Programming in Java",
    hours: "100h",
    institution: "IFSC - Santa Catarina - SC",
    country: "Brazil",
    year: "2018",
    skills: ["Java", "Spring Boot", "Hibernate"],
  },
  {
    title: "Arduino – Basic Level",
    hours: "28h",
    institution: "IFSC - Santa Catarina- SC",
    country: "Brazil",
    year: "2017",
    skills: ["C Language", "Microcontrollers"],
  },

  {
    title: "Microcomputer Support and Maintenance",
    hours: "72h",
    institution: "IFSC - Santa Catarina-SC",
    country: "Brazil",
    year: "2016",
  },
  {
    title: "Introduction to Computer Programming",
    hours: "80h",
    institution: "IFSC - Santa Catarina - SC",
    country: "Brazil",
    year: "2016",
    skills: ["C", "Python", "HTML", "CSS", "JavaScript", "SQL"],
  },
  {
    title: "Microcomputer Operator",
    hours: "60h",
    institution: "ABELHA-RAINHA - Simplício Mendes-PI",
    country: "Brazil",
    year: "2010",
    skills: ["Linux", "Office tools", "Internet basics"],
  },
];

const ACADEMIC: Academic[] = [
  { title: "Technical Degree in Electrotechnics – 4th Semester (2017–2019)" },
  { title: "Systems Development Technician – Locked (2021)" },
  { title: "Industrial Electronics Technologist – Locked (2021)" },
];

const Education: React.FC = () => {
  const [openCourse, setOpenCourse] = useState<Course | null>(null);

  return (
    <>
      {/* ACADEMIC */}
      <Section
        title="Academic Education"
        subtitle="Formal education background"
      >
        <div
          className="grid gap-2"
          style={{
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
          }}
        >
          {ACADEMIC.map(a => (
            <div
              key={a.title}
              className="ds-card ds-card-pad text-sm font-medium"
            >
              {a.title}
            </div>
          ))}
        </div>
      </Section>


      {/* COURSES */}
      <Section
        title="Qualification Courses"
        subtitle="Professional and technical training"
      >
        <div
          className="grid gap-2"
          style={{ gridTemplateColumns: "repeat(auto-fit, minmax(420px, 1fr))" }}
        >
          {COURSES.map(c => (
            <article
              key={c.title}
              className="ds-card ds-card-pad transition hover:-translate-y-1 hover:shadow-lg"
            >
            <h3 className="text-sm font-semibold leading-snug">
              {c.title}
            </h3>
            <p className="text-xs text-[var(--muted)] mt-1">
              {c.hours} • {c.year}
            </p>

            <Button
              className="mt-4 text-xs ds-btn-primary"
              onClick={() => setOpenCourse(c)}
            >
              View details →
            </Button>

            </article>
          ))}
        </div>
      </Section>

      {/* EVENTS */}
      <Section
        title="Events & Lectures"
        subtitle="Technical talks, seminars and short courses"
      >
        <div
          className="grid gap-2"
          style={{
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
          }}
        >
          {EVENTS.map(e => (
            <div key={e.title} className="ds-card-event">
              <h4 className="text-sm font-semibold leading-snug">
                {e.title}
              </h4>
              <span className="mt-1 text-xs text-[var(--muted)]">
                {e.hours}
              </span>
            </div>
          ))}
        </div>
      </Section>



      {/* MODAL */}
      <Modal
        open={!!openCourse}
        title={openCourse?.title || ""}
        onClose={() => setOpenCourse(null)}
      >
        {openCourse && (
          <div className="space-y-6">

            {/* META GRID */}
            <div className="grid grid-cols-2 gap-x-6 gap-y-2 text-sm text-[var(--muted)]">
              <div><strong>Institution:</strong> {openCourse.institution}</div>
              <div><strong>Year:</strong> {openCourse.year}</div>

              <div><strong>Hours:</strong> {openCourse.hours || "N/A"}</div>
              {openCourse.country && (
                <div><strong>Country:</strong> {openCourse.country}</div>
              )}

              {openCourse.type && (
                <div><strong>Type:</strong> {openCourse.type}</div>
              )}
              {openCourse.mode && (
                <div><strong>Mode:</strong> {openCourse.mode}</div>
              )}
            </div>

            {/* DESCRIPTION */}
            {openCourse.description && (
              <p className="text-sm text-[var(--muted)] leading-relaxed">
                {openCourse.description}
              </p>
            )}

            {/* SKILLS */}
            {openCourse.skills && (
              <div>
                <h4 className="mb-2 text-xs font-semibold tracking-wide text-[var(--text)]">
                  Skills & Topics
                </h4>
                <div className="flex flex-wrap gap-2">
                  {openCourse.skills.map(s => (
                    <span key={s} className="ds-chip">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* ACTIONS */}
            {openCourse.credentialUrl && (
              <div className="pt-4 border-t border-[var(--border)] flex justify-end">
                <a
                  href={openCourse.credentialUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="ds-btn ds-btn-primary text-xs"
                >
                  View credential ↗
                </a>
              </div>
            )}
          </div>
        )}
      </Modal>


    </>
  );
};

export default Education;
