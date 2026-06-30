import React from "react";
import {
  FaServer,
  FaNetworkWired,
  FaShieldAlt,
  FaCodeBranch,
  FaCloud,
} from "react-icons/fa";

const Infra = () => {
  return (
    <div className="min-h-screen p-6 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold text-center text-teal-400 mb-16">
        Infraestrutura DevOps
      </h1>

      <div className="space-y-10 max-w-4xl mx-auto">
        {sections.map((section, index) => (
          <div
            key={index}
            className="bg-gray-800 p-6 rounded-xl shadow hover:shadow-lg transition"
          >
            <h2 className="text-xl font-bold flex items-center mb-4">
              {section.icon}
              {section.title}
            </h2>
            <ul className="list-disc list-inside pl-2 space-y-1 text-gray-300 text-base leading-relaxed">
              {section.items.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Infra;
