'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import ChatContainer from '../../components/chat/ChatContainer';
import Sidebar from '../../components/ui/Sidebar';
import { Message } from '../../lib/types';
import { createDefaultSessionTitle, loadHistory, persistMessage } from '../../lib/storage';
import SettingsPanel from '../../components/ui/SettingsPanel';
import SearchBar from '../../components/ui/SearchBar';

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string>('default');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const abortController = useRef<AbortController | null>(null);

  useEffect(() => {
    loadHistory(sessionId).then(setMessages).catch(() => setMessages([]));
  }, [sessionId]);

  const title = useMemo(() => createDefaultSessionTitle(messages), [messages]);

  const handleSend = async (content: string, files: File[]) => {
    const newMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      createdAt: new Date().toISOString(),
      attachments: files.map((file) => ({
        id: crypto.randomUUID(),
        name: file.name,
        type: file.type,
        size: file.size,
      })),
    };

    const nextMessages = [...messages, newMessage];
    setMessages(nextMessages);
    persistMessage(sessionId, newMessage);

    abortController.current?.abort();
    abortController.current = new AbortController();

    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        messages: nextMessages,
        sessionId,
      }),
      signal: abortController.current.signal,
    });

    if (!response.body) {
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let assistantMessage: Message = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      createdAt: new Date().toISOString(),
    };

    setMessages((current) => [...current, assistantMessage]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      assistantMessage = {
        ...assistantMessage,
        content: assistantMessage.content + chunk,
      };
      setMessages((current) => {
        const updated = [...current];
        updated[updated.length - 1] = assistantMessage;
        return updated;
      });
    }

    persistMessage(sessionId, assistantMessage);
  };

  return (
    <div className="flex h-screen bg-surface">
      <Sidebar
        activeSession={sessionId}
        title={title}
        onSelectSession={setSessionId}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />
      <main className="flex flex-1 flex-col">
        <SearchBar />
        <ChatContainer
          messages={messages}
          onSend={handleSend}
          onCancel={() => abortController.current?.abort()}
        />
      </main>
      <SettingsPanel open={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
    </div>
  );
}
