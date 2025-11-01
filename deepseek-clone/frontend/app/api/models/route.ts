import { NextResponse } from 'next/server';

const MODELS = [
  { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', contextWindow: 128000 },
  { id: 'deepseek-reasoner', name: 'DeepSeek Reasoner', contextWindow: 131072 },
  { id: 'deepseek-coder', name: 'DeepSeek Coder', contextWindow: 65536 },
];

export async function GET() {
  return NextResponse.json({ models: MODELS });
}
