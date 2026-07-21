import type { Summary, Note, TranscriptLine, OcrEntry, CodeSnippet, QuizQuestion } from '@/types/content.types';

// Mocks
export const getSummary = async (_id: string): Promise<Summary> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: 'sum1',
        videoId: _id,
        overview: 'This video covers the basics of React Query.',
        keyPoints: ['Fetching', 'Caching', 'Mutations'],
      });
    }, 500);
  });
};

export const getNotes = async (_id: string): Promise<Note[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 'n1', videoId: _id, timestamp: 10, content: 'Introduction to data fetching.' },
        { id: 'n2', videoId: _id, timestamp: 45, content: 'Setting up the QueryClient.' },
      ]);
    }, 500);
  });
};

export const getTranscript = async (_id: string): Promise<TranscriptLine[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { start: 0, end: 5, text: 'Hello everyone.' },
        { start: 5, end: 10, text: 'Today we will talk about React.' },
      ]);
    }, 500);
  });
};

export const getOcrArchive = async (_id: string): Promise<OcrEntry[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { timestamp: 15, text: 'const a = 1;' },
      ]);
    }, 500);
  });
};

export const getReconstructedCode = async (_id: string): Promise<CodeSnippet[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { language: 'typescript', code: 'const a = 1;\nconsole.log(a);', timestamp: 15 },
      ]);
    }, 500);
  });
};

export const getQuiz = async (_id: string): Promise<QuizQuestion[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        {
          id: 'q1',
          question: 'What does React Query manage?',
          options: ['UI State', 'Server State', 'CSS Classes'],
          correctOptionIndex: 1,
          explanation: 'React Query is designed for asynchronous server state management.',
        }
      ]);
    }, 500);
  });
};
