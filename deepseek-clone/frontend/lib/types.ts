export interface AttachmentMeta {
  id: string;
  name: string;
  type: string;
  size: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  createdAt: string;
  attachments?: AttachmentMeta[];
}

export interface StoredSettings {
  model: string;
  temperature: number;
  voiceEnabled: boolean;
}

export interface ChatRequest {
  messages: Message[];
  sessionId: string;
  model?: string;
  temperature?: number;
}
