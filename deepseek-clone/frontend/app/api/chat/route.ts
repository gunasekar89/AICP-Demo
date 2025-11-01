import { NextRequest } from 'next/server';
import { ChatRequest, Message } from '../../../lib/types';

const SYSTEM_PROMPT = `You are DeepSeek, an elite research assistant. Provide concise, well-structured answers.
When the user shares files mention how they will be analysed.
If code is provided, explain, lint, and offer improvements.`;

export async function POST(request: NextRequest) {
  const payload = (await request.json()) as ChatRequest;
  const controller = new ReadableStream({
    async start(streamController) {
      const encoder = new TextEncoder();
      const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
      const assistant: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: '',
        createdAt: new Date().toISOString(),
      };

      const lastMessage = payload.messages[payload.messages.length - 1];
      const content = [SYSTEM_PROMPT, lastMessage?.content ?? ''].join('\n\n');
      const words = content.split(/\s+/);
      for (const word of words) {
        assistant.content += `${word} `;
        streamController.enqueue(encoder.encode(`${word} `));
        await delay(25);
      }
      streamController.close();
    },
  });

  return new Response(controller, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-cache',
    },
  });
}
