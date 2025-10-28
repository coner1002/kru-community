'use client';

import { useState, useEffect } from 'react';

type LanguageMode = 'ko' | 'ru' | 'both';

export default function LanguageSwitcher() {
  const [langMode, setLangMode] = useState<LanguageMode>('both');

  useEffect(() => {
    // 저장된 언어 설정 불러오기
    const saved = localStorage.getItem('preferredLang') as LanguageMode;
    if (saved) {
      setLangMode(saved);
      document.body.setAttribute('data-lang', saved);
    }
  }, []);

  const handleLanguageChange = (mode: LanguageMode) => {
    setLangMode(mode);
    document.body.setAttribute('data-lang', mode);
    localStorage.setItem('preferredLang', mode);
  };

  return (
    <div className="flex gap-1">
      <button
        onClick={() => handleLanguageChange('ko')}
        className={`px-2 py-1 text-xs font-medium rounded border transition-all ${
          langMode === 'ko'
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
        }`}
        title="한국어만 표시"
      >
        한국어
      </button>
      <button
        onClick={() => handleLanguageChange('ru')}
        className={`px-2 py-1 text-xs font-medium rounded border transition-all ${
          langMode === 'ru'
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
        }`}
        title="Показать только русский"
      >
        Русский
      </button>
      <button
        onClick={() => handleLanguageChange('both')}
        className={`px-2 py-1 text-xs font-medium rounded border transition-all ${
          langMode === 'both'
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
        }`}
        title="한국어+러시아어"
      >
        한국어+Русский
      </button>
    </div>
  );
}
