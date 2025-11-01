import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  const session = cookies().get('deepseek-session');
  return NextResponse.json({ session: session?.value ?? 'default' });
}

export async function DELETE(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const sessionId = searchParams.get('sessionId');
  if (!sessionId) {
    return NextResponse.json({ error: 'Missing sessionId' }, { status: 400 });
  }
  cookies().delete('deepseek-session');
  return NextResponse.json({ deleted: sessionId });
}
