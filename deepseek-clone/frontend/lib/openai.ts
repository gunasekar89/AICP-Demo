import { ChatRequest, Message } from './types';

export async function createChatCompletion(payload: ChatRequest): Promise<Message> {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch completion');
  }

  const data = await response.json();
  return data.message as Message;
}
