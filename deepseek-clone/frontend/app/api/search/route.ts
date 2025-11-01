import { NextRequest, NextResponse } from 'next/server';

const MOCK_RESULTS = [
  'Latest research insights gathered from trusted publications.',
  'Key statistics summarised with citations for rapid review.',
  'Related code examples sourced from community repositories.',
];

export async function POST(request: NextRequest) {
  const { query } = await request.json();
  if (!query || typeof query !== 'string') {
    return NextResponse.json({ error: 'Missing query' }, { status: 400 });
  }

  const results = MOCK_RESULTS.map((result, index) => `${result} (Result ${index + 1} for "${query}")`);
  return NextResponse.json({ results });
}
