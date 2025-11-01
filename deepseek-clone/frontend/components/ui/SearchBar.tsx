'use client';

import { useState } from 'react';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    const response = await fetch('/api/search', {
      method: 'POST',
      body: JSON.stringify({ query }),
    });
    const data = await response.json();
    setResults(data.results ?? []);
    setLoading(false);
  };

  return (
    <div className="border-b border-default bg-background p-4">
      <form onSubmit={handleSubmit} className="flex items-center gap-3">
        <input
          type="text"
          className="flex-1 rounded-lg border border-default bg-surface px-3 py-2 text-sm"
          placeholder="Search the web to enrich the conversation"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <button
          type="submit"
          className="rounded-lg bg-[var(--primary)] px-4 py-2 text-sm font-semibold text-white hover:bg-[var(--primary-dark)]"
        >
          {loading ? 'Searching…' : 'Search'}
        </button>
      </form>
      {results.length > 0 && (
        <div className="mt-3 grid gap-2 text-sm text-secondary md:grid-cols-3">
          {results.map((result) => (
            <div key={result} className="rounded-lg border border-default bg-surface p-3">
              {result}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
