import { Message, StoredSettings } from './types';

const MESSAGE_KEY_PREFIX = 'deepseek-session';
const SETTINGS_KEY = 'deepseek-settings';

export async function persistMessage(sessionId: string, message: Message) {
  const key = `${MESSAGE_KEY_PREFIX}:${sessionId}`;
  const existing = await loadHistory(sessionId);
  const updated = [...existing, message];
  if (typeof window !== 'undefined') {
    localStorage.setItem(key, JSON.stringify(updated));
  }
}

export async function loadHistory(sessionId: string): Promise<Message[]> {
  if (typeof window === 'undefined') return [];
  const key = `${MESSAGE_KEY_PREFIX}:${sessionId}`;
  const data = localStorage.getItem(key);
  return data ? (JSON.parse(data) as Message[]) : [];
}

export async function listSessions(): Promise<string[]> {
  if (typeof window === 'undefined') return [];
  return Object.keys(localStorage)
    .filter((key) => key.startsWith(MESSAGE_KEY_PREFIX))
    .map((key) => key.replace(`${MESSAGE_KEY_PREFIX}:`, ''));
}

export async function loadSettings(): Promise<StoredSettings | null> {
  if (typeof window === 'undefined') return null;
  const data = localStorage.getItem(SETTINGS_KEY);
  return data ? (JSON.parse(data) as StoredSettings) : null;
}

export async function saveSettings(settings: StoredSettings) {
  if (typeof window === 'undefined') return;
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

export function createDefaultSessionTitle(messages: Message[]): string {
  if (messages.length === 0) {
    return 'New conversation';
  }

  const lastUserMessage = [...messages].reverse().find((message) => message.role === 'user');
  if (!lastUserMessage) {
    return 'Conversation';
  }

  return lastUserMessage.content.slice(0, 40) + (lastUserMessage.content.length > 40 ? '…' : '');
}
