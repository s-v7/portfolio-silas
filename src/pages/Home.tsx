import { useEffect } from "react";
import Hero from "../components/Hero";
import SkillCards from "../components/SkillCards";
import WhatIDo from "../components/WhatIDo";
import CTASection from "../components/CTASection";

export default function Home() {
  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) e.target.classList.add("visible");
        }),
      { threshold: 0.08, rootMargin: "0px 0px -40px 0px" },
    );
    document.querySelectorAll(".reveal").forEach((el) => obs.observe(el));
    return () => obs.disconnect();
  }, []);
  return (
    <main>
      <Hero />
      <SkillCards />
      <WhatIDo />
      <CTASection />
    </main>
  );
}
