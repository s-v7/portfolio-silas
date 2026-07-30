export type AnalyticsItem = {
  total: number;
};

export type ProviderAnalytics = AnalyticsItem & {
  provider: string;
};

export type IntentAnalytics = AnalyticsItem & {
  intent: string;
};

export type TimelineAnalytics = AnalyticsItem & {
  day: string;
};

export type KnowledgeGap = {
  id: string;
  intent: string;
  question: string;
  provider: string;
  comment: string | null;
  created_at: string;
};

export type AnalyticsResponse = {
  summary: {
    totalInteractions: number;
    totalIntents: number;
    totalFeedback: number;
    positive: number;
    negative: number;
    positiveRate: number;
    lastInteraction: string | null;
  };
  providers: ProviderAnalytics[];
  intents: IntentAnalytics[];
  timeline: TimelineAnalytics[];
  knowledgeGaps: KnowledgeGap[];
};
