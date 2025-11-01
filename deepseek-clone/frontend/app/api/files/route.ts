import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const summaries: Record<string, string> = {};

  formData.forEach((value, key) => {
    if (value instanceof File) {
      summaries[value.name] = `Processed ${key} (${value.type}) with ${value.size} bytes.`;
    }
  });

  return NextResponse.json({ summaries });
}
