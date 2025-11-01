'use client';

import { useEffect, useState } from 'react';
import { listSessions } from '../../lib/storage';

interface Props {
  activeSession: string;
  title: string;
  onSelectSession: (sessionId: string) => void;
  onOpenSettings: () => void;
}

export default function Sidebar({ activeSession, title, onSelectSession, onOpenSettings }: Props) {
  const [sessions, setSessions] = useState<string[]>([]);

  useEffect(() => {
    listSessions().then(setSessions);
  }, []);

  return (
    <aside className="hidden w-72 flex-col border-r border-default bg-background p-4 lg:flex">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-secondary">Current session</p>
          <p className="text-lg font-semibold text-primary">{title}</p>
        </div>
        <button
          onClick={onOpenSettings}
          className="rounded-lg border border-default px-3 py-1 text-xs font-semibold text-secondary hover:bg-surface"
        >
          Settings
        </button>
      </div>
      <p className="text-xs font-semibold uppercase tracking-wide text-secondary">History</p>
      <ul className="mt-3 space-y-2 text-sm text-secondary">
        {sessions.map((sessionId) => (
          <li key={sessionId}>
            <button
              onClick={() => onSelectSession(sessionId)}
              className={`w-full rounded-lg px-3 py-2 text-left transition ${
                activeSession === sessionId ? 'bg-surface text-primary' : 'hover:bg-surface'
              }`}
            >
              {sessionId}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
