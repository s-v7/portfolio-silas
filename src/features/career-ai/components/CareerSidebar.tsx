import { Props } from "../../../data/careerSidebar";

import { KnowledgeBase } from "./KnowledgeBase";
import { AITools } from "./AITools";

export function CareerSidebar({ loading, onPrompt }: Readonly<Props>) {
  return (
    <aside className="career-sidebar">
      <KnowledgeBase loading={loading} onSelect={onPrompt} />
      <AITools loading={loading} onSelect={onPrompt} />
    </aside>
  );
}
