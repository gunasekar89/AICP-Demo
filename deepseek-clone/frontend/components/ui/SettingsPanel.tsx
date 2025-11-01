'use client';

import { useEffect, useState } from 'react';
import { loadSettings, saveSettings } from '../../lib/storage';

interface Props {
  open: boolean;
  onClose: () => void;
}

const AVAILABLE_MODELS = [
  { id: 'gpt-4-turbo', name: 'GPT-4 Turbo' },
  { id: 'deepseek-reasoner', name: 'DeepSeek Reasoner' },
  { id: 'deepseek-coder', name: 'DeepSeek Coder' },
];

export default function SettingsPanel({ open, onClose }: Props) {
  const [model, setModel] = useState(AVAILABLE_MODELS[0].id);
  const [temperature, setTemperature] = useState(0.7);
  const [voiceEnabled, setVoiceEnabled] = useState(false);

  useEffect(() => {
    if (!open) return;
    loadSettings().then((settings) => {
      if (settings) {
        setModel(settings.model);
        setTemperature(settings.temperature);
        setVoiceEnabled(settings.voiceEnabled);
      }
    });
  }, [open]);

  const handleSave = () => {
    saveSettings({ model, temperature, voiceEnabled });
    onClose();
  };

  return (
    <div
      className={`fixed inset-y-0 right-0 z-20 w-80 transform bg-background p-6 shadow-xl transition-transform duration-300 ${
        open ? 'translate-x-0' : 'translate-x-full'
      }`}
    >
      <h2 className="text-xl font-semibold text-primary">Settings</h2>
      <p className="mt-1 text-sm text-secondary">Control the behaviour of the assistant.</p>
      <div className="mt-6 space-y-4 text-sm">
        <label className="block">
          <span className="text-xs uppercase tracking-wide text-secondary">Model</span>
          <select
            value={model}
            onChange={(event) => setModel(event.target.value)}
            className="mt-1 w-full rounded-lg border border-default bg-surface p-2"
          >
            {AVAILABLE_MODELS.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="text-xs uppercase tracking-wide text-secondary">Creativity</span>
          <input
            type="range"
            min={0}
            max={1}
            step={0.1}
            value={temperature}
            onChange={(event) => setTemperature(Number(event.target.value))}
            className="mt-1 w-full"
          />
          <span className="text-xs text-secondary">{temperature.toFixed(1)}</span>
        </label>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={voiceEnabled}
            onChange={(event) => setVoiceEnabled(event.target.checked)}
          />
          <span>Enable voice input/output</span>
        </label>
      </div>
      <div className="mt-6 flex justify-end gap-3">
        <button onClick={onClose} className="rounded-lg border border-default px-4 py-2 text-sm text-secondary">
          Cancel
        </button>
        <button
          onClick={handleSave}
          className="rounded-lg bg-[var(--primary)] px-4 py-2 text-sm font-semibold text-white hover:bg-[var(--primary-dark)]"
        >
          Save
        </button>
      </div>
    </div>
  );
}
