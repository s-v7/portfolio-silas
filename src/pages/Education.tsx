import { useState } from "react";

interface Course {
  title: string;
  hours: string;
  institution: string;
  country: string;
  year: string;
  skills?: string[];
}

interface Event {
  title: string;
  hours: string;
}

interface Academic {
  title: string;
}

const EVENTS: Event[] = [
  {
    title:
      "SNCT Lecture 2019: Sustainable Stingless Beekeeping (ASF)",
    hours: "6h",
  },
  {
    title:
      "SNCT Catarinense 2021 – Thematic Table with external extensionist entities and students",
    hours: "3h",
  },
  {
    title:
      "Co-designing application-specific quantum accelerators for HPC",
    hours: "1h",
  },
  {
    title:
      "7º Teaching, Research, Extension and Innovation Seminar IFSC (SEPEI 2018)",
    hours: "27h",
  },
  {
    title: "Lecture: 5G and IoT Connectivity",
    hours: "2h",
  },
  {
    title: "Progress in Photonic Quantum Computing",
    hours: "1h",
  },
  {
    title: "Minicourse: Introduction to quantum information using Qiskit",
    hours: "4h",
  },
];

const COURSES: Course[] = [
  {
    title: "Microcomputer Operator",
    hours: "60h",
    institution: "IFSC - Santa Catarina",
    country: "Brazil",
    year: "2010",
    skills: [
      "Linux",
      "Typing notions",
      "Office tools",
      "Internet basics",
    ],
  },
  {
    title: "Microcomputer Support and Maintenance",
    hours: "72h",
    institution: "IFSC - Santa Catarina",
    country: "Brazil",
    year: "2016",
  },
  {
    title: "Object Oriented Programming in Java",
    hours: "100h",
    institution: "IFSC - Santa Catarina",
    country: "Brazil",
    year: "2018",
  },
  {
    title: "Linux Computer Network Configuration",
    hours: "60h",
    institution: "IFSC - Santa Catarina",
    country: "Brazil",
    year: "2021",
  },
  {
    title: "Front End Programming",
    hours: "40h",
    institution: "IFSC - Santa Catarina",
    country: "Brazil",
    year: "2021",
  },
  {
    title: "Back End Programming",
    hours: "60h",
    institution: "IFSC - Santa Catarina",
    country: "Brazil",
    year: "2021",
  },
  {
    title: "Database Fundamentals",
    hours: "40h",
    institution: "IFSC - Santa Catarina",
    country: "Brazil",
    year: "2021",
  },
];

const ACADEMIC: Academic[] = [
  {
    title:
      "Technical Degree in Electrotechnics – 4th Semester (2017–2019)",
  },
  {
    title:
      "Systems Development Technician – Locked (2021)",
  },
  {
    title:
      "Industrial Electronics Technologist – Locked (2021)",
  },
];


const Education: React.FC = () => {
  const [openCourse, setOpenCourse] = useState<Course | null>(null);

  return (
    <section className="mx-auto max-w-5xl px-4 py-10 text-slate-200">
      {/* EVENTS */}
      <section className="mb-10">
        <h2 className="text-2xl font-bold mb-4">
          Participation in Events & Lectures
        </h2>
        <ul className="space-y-2 text-slate-300">
          {EVENTS.map((e) => (
            <li key={e.title}>
              • {e.title} — <span className="text-slate-400">{e.hours}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* COURSES */}
      <section className="mb-10">
        <h2 className="text-2xl font-bold mb-4">
          Qualification Courses
        </h2>

        <ul className="space-y-3">
          {COURSES.map((c) => (
            <li key={c.title} className="flex flex-wrap gap-2 items-center">
              <span className="font-semibold">
                {c.title} — {c.hours}
              </span>

              <button
                onClick={() => setOpenCourse(c)}
                className="rounded bg-indigo-500 px-3 py-1 text-xs font-semibold text-white hover:bg-indigo-600"
              >
                Details
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* ACADEMIC */}
      <section className="mb-10">
        <h2 className="text-2xl font-bold mb-4">
          Academic Education
        </h2>
        <ul className="space-y-2 text-slate-300">
          {ACADEMIC.map((a) => (
            <li key={a.title}>• {a.title}</li>
          ))}
        </ul>
      </section>

      {/* MODAL */}
      {openCourse && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
          <div className="max-w-md rounded-xl bg-slate-900 p-6 ring-1 ring-white/10">
            <h3 className="text-lg font-bold mb-2">
              {openCourse.title}
            </h3>

            <p className="text-sm text-slate-300">
              <strong>Institution:</strong>{" "}
              {openCourse.institution}
              <br />
              <strong>Country:</strong>{" "}
              {openCourse.country}
              <br />
              <strong>Year:</strong> {openCourse.year}
            </p>

            {openCourse.skills && (
              <ul className="mt-3 list-disc pl-5 text-sm text-slate-300">
                {openCourse.skills.map((s) => (
                  <li key={s}>{s}</li>
                ))}
              </ul>
            )}

            <button
              onClick={() => setOpenCourse(null)}
              className="mt-4 rounded bg-slate-700 px-4 py-2 text-sm hover:bg-slate-600"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </section>
  );
};

export default Education;

