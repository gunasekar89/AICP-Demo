'use client';

import { useEffect, useRef, useState } from 'react';
import autoAnimate from '@formkit/auto-animate';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import FileUploadZone from '../file/FileUploadZone';
import MessageBubble from './MessageBubble';
import { Message } from '../../lib/types';

interface Props {
  messages: Message[];
  onSend: (content: string, files: File[]) => Promise<void>;
  onCancel: () => void;
}

export default function ChatContainer({ messages, onSend, onCancel }: Props) {
  const [input, setInput] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const listRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (listRef.current) {
      autoAnimate(listRef.current);
    }
  }, []);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!input.trim() && files.length === 0) return;
    await onSend(input, files);
    setInput('');
    setFiles([]);
  };

  return (
    <div className="flex flex-1 flex-col overflow-hidden">
      <div ref={listRef} className="flex-1 space-y-4 overflow-y-auto p-6">
        {messages.map((message) => (
          <MessageBubble key={message.id} role={message.role}>
            <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>{message.content}</ReactMarkdown>
          </MessageBubble>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="border-t border-default bg-background p-4">
        <FileUploadZone files={files} onFilesChange={setFiles} />
        <textarea
          className="mt-3 w-full resize-none rounded-lg border border-default bg-surface p-3 shadow-sm focus:border-primary focus:outline-none"
          rows={3}
          placeholder="Ask DeepSeek anything..."
          value={input}
          onChange={(event) => setInput(event.target.value)}
        />
        <div className="mt-3 flex justify-between">
          <button
            type="button"
            onClick={onCancel}
            className="rounded-lg border border-default px-4 py-2 text-sm text-secondary hover:bg-surface/80"
          >
            Stop
          </button>
          <button
            type="submit"
            className="rounded-lg bg-[var(--primary)] px-4 py-2 text-sm font-semibold text-white hover:bg-[var(--primary-dark)]"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
