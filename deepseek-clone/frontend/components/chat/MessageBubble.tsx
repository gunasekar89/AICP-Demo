import { ReactNode } from 'react';

interface Props {
  role: 'user' | 'assistant' | 'system';
  children: ReactNode;
}

const styles: Record<Props['role'], string> = {
  user: 'bg-[var(--primary)] text-white self-end ml-auto',
  assistant: 'bg-surface text-primary border border-default',
  system: 'bg-yellow-50 text-yellow-900 border border-yellow-200',
};

export default function MessageBubble({ role, children }: Props) {
  return (
    <div className={`max-w-2xl whitespace-pre-wrap rounded-2xl px-4 py-3 shadow-sm ${styles[role]}`}>
      {children}
    </div>
  );
}
