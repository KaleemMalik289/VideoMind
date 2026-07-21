export interface Summary {
  id: string;
  videoId: string;
  overview: string;
  keyPoints: string[];
}

export interface Note {
  id: string;
  videoId: string;
  timestamp: number;
  content: string;
}

export interface TranscriptLine {
  start: number;
  end: number;
  text: string;
}

export interface OcrEntry {
  timestamp: number;
  text: string;
  boundingBox?: unknown;
}

export interface CodeSnippet {
  language: string;
  code: string;
  timestamp: number;
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctOptionIndex: number;
  explanation: string;
}
