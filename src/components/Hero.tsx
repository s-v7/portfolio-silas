import Hero from "../components/Hero";
import WhatIDo from "../components/WhatIDo";
import Stack from "../components/Stack";
import CTASection from "../components/CTASection";

const Home: React.FC = () => {
  return (
    <>
      <a href="#main" className="skip-link">
        Pular para o conteúdo
      </a>

      <main id="main">
        <Hero />
        <WhatIDo />
        <Stack />
        <CTASection />
      </main>
    </>
  );
};

export default Home;

