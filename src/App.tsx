import { useState } from "react";
import ArchitectureHero from "./components/ArchitectureHero";
import ArchitectureOverview from "./components/ArchitectureOverview";
import DomainBoundaries from "./components/DomainBoundaries";
import TechnologyStack from "./components/TechnologyStack";
import EngineeringPrinciples from "./components/EngineeringPrinciples";
import ImplementationStages from "./components/ImplementationStages";
import SystemData from "./components/SystemData";
import Workspace from "./components/Workspace";
import Footer from "./components/Footer";

export default function App() {
  const [activeSection, setActiveSection] = useState("overview");

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 font-mono">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-950/90 backdrop-blur-md border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded bg-emerald-500/20 flex items-center justify-center">
                <span className="text-emerald-400 text-sm font-bold">E</span>
              </div>
              <span className="text-sm font-semibold text-gray-200">
                ERP Platform
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Architecture
              </span>
            </div>
            <div className="hidden md:flex items-center gap-1">
              {[
                { id: "overview", label: "Overview" },
                { id: "architecture", label: "Architecture" },
                { id: "domains", label: "Domains" },
                { id: "technology", label: "Technology" },
                { id: "principles", label: "Principles" },
                { id: "stages", label: "Stages" },
                { id: "data", label: "System Data" },
                { id: "workspace", label: "Workspace" },
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveSection(item.id);
                    document
                      .getElementById(item.id)
                      ?.scrollIntoView({ behavior: "smooth" });
                  }}
                  className={`px-3 py-1.5 text-xs rounded transition-colors ${
                    activeSection === item.id
                      ? "bg-gray-800 text-emerald-400"
                      : "text-gray-400 hover:text-gray-200 hover:bg-gray-800/50"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-14">
        <ArchitectureHero />
        <section id="architecture">
          <ArchitectureOverview />
        </section>
        <section id="domains">
          <DomainBoundaries />
        </section>
        <section id="technology">
          <TechnologyStack />
        </section>
        <section id="principles">
          <EngineeringPrinciples />
        </section>
        <section id="stages">
          <ImplementationStages />
        </section>
        <section id="data">
          <SystemData />
        </section>
        <section id="workspace">
          <Workspace />
        </section>
        <Footer />
      </main>
    </div>
  );
}
