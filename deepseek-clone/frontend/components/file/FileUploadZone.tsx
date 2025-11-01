'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface Props {
  files: File[];
  onFilesChange: (files: File[]) => void;
}

export default function FileUploadZone({ files, onFilesChange }: Props) {
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (accepted: File[], rejected: File[]) => {
      if (rejected.length > 0) {
        setError('Some files were rejected. Only documents, images, and code files are supported.');
        return;
      }
      setError(null);
      onFilesChange([...files, ...accepted]);
    },
    [files, onFilesChange],
  );

  const removeFile = (index: number) => {
    const next = [...files];
    next.splice(index, 1);
    onFilesChange(next);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'image/*': ['.png', '.jpg', '.jpeg'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md'],
      'application/json': ['.json'],
    },
  });

  return (
    <div>
      <div
        {...getRootProps()}
        className={`flex cursor-pointer items-center justify-center rounded-lg border-2 border-dashed border-default p-4 text-sm transition hover:border-[var(--primary)] ${isDragActive ? 'bg-surface/80' : ''}`}
      >
        <input {...getInputProps()} />
        <span>{isDragActive ? 'Drop files here' : 'Drag & drop files or click to upload'}</span>
      </div>
      {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
      {files.length > 0 && (
        <ul className="mt-3 space-y-2 text-sm text-secondary">
          {files.map((file, index) => (
            <li key={file.name} className="flex items-center justify-between rounded border border-default px-3 py-2">
              <span>{file.name}</span>
              <button type="button" onClick={() => removeFile(index)} className="text-xs text-red-500 hover:underline">
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
