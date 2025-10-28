'use client';

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { createPost, PostCreate, detectLanguage } from '@/lib/api/posts';

// Rich Text Editor 동적 import
const RichTextEditor = dynamic(() => import('./rich-text-editor'), {
  ssr: false,
  loading: () => <div className="h-64 bg-gray-100 animate-pulse rounded-md"></div>
});

interface PostEditorV2Props {
  categoryId: number;
  onSuccess?: (postId: number) => void;
  onCancel?: () => void;
}

export default function PostEditorV2({ categoryId, onSuccess, onCancel }: PostEditorV2Props) {
  const [title, setTitle] = useState('');
  const [translatedTitle, setTranslatedTitle] = useState('');
  const [content, setContent] = useState('');
  const [summary, setSummary] = useState('');
  const [tags, setTags] = useState('');
  const [allowComments, setAllowComments] = useState(true);
  const [autoTranslate, setAutoTranslate] = useState(true);
  const [detectedLang, setDetectedLang] = useState<'ko' | 'ru'>('ko');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState('');

  // 언어 자동 감지
  useEffect(() => {
    if (title || content) {
      // HTML 태그 제거 후 언어 감지
      const plainContent = content.replace(/<[^>]*>/g, '');
      const textToCheck = title + ' ' + plainContent;
      const detected = detectLanguage(textToCheck);
      if (detected === 'ko' || detected === 'ru') {
        setDetectedLang(detected);
      }
    }
  }, [title, content]);

  // 제목 실시간 번역 미리보기 (옵션)
  const handleTitleTranslate = async () => {
    if (!title.trim() || !autoTranslate) return;

    setIsTranslating(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/translate/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: title,
          target_lang: detectedLang === 'ko' ? 'ru' : 'ko',
          source_lang: detectedLang
        })
      });

      if (response.ok) {
        const data = await response.json();
        setTranslatedTitle(data.translated_text);
      }
    } catch (err) {
      console.error('제목 번역 실패:', err);
    } finally {
      setIsTranslating(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      // HTML 태그 제거 후 요약 생성 (요약이 없는 경우)
      const plainContent = content.replace(/<[^>]*>/g, '');
      const autoSummary = summary.trim() || plainContent.substring(0, 200);

      const postData: PostCreate = {
        title: title.trim(),
        content: content,  // HTML 포함된 내용 그대로 전송
        summary: autoSummary,
        category_id: categoryId,
        tags: tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        allow_comments: allowComments,
        source_lang: detectedLang,
        auto_translate: autoTranslate,
      };

      console.log('게시글 작성 요청:', postData);

      const result = await createPost(postData);

      console.log('게시글 작성 성공:', result);

      if (onSuccess) {
        onSuccess(result.id);
      }
    } catch (err: any) {
      console.error('게시글 작성 실패:', err);
      setError(err.response?.data?.detail || err.message || '게시글 작성 중 오류가 발생했습니다.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">새 게시글 작성</h2>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
          <strong>오류:</strong> {error}
        </div>
      )}

      {/* 언어 감지 및 번역 옵션 */}
      <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="font-medium">감지된 언어: </span>
            <span className="text-blue-700 font-bold">
              {detectedLang === 'ko' ? '🇰🇷 한국어' : '🇷🇺 러시아어'}
            </span>
          </div>
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={autoTranslate}
              onChange={(e) => setAutoTranslate(e.target.checked)}
              className="mr-2 w-4 h-4"
            />
            <span className="text-sm font-medium">
              {detectedLang === 'ko' ? '러시아어로 자동 번역' : '한국어로 자동 번역'}
            </span>
          </label>
        </div>
        {autoTranslate && (
          <div className="text-sm text-gray-600">
            ℹ️ 게시글 등록 시 DeepL API를 사용하여 자동으로 번역됩니다.
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* 제목 입력 (단일 언어) */}
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
            제목 ({detectedLang === 'ko' ? '한국어' : '러시아어'}) <span className="text-red-500">*</span>
          </label>
          <div className="space-y-2">
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              onBlur={handleTitleTranslate}
              placeholder={detectedLang === 'ko' ? '게시글 제목을 입력하세요' : 'Введите заголовок статьи'}
              required
              maxLength={255}
              className="w-full px-4 py-3 text-lg border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />

            {/* 번역된 제목 미리보기 */}
            {autoTranslate && translatedTitle && (
              <div className="p-3 bg-green-50 border border-green-200 rounded-md">
                <div className="text-sm text-green-700 mb-1">
                  {detectedLang === 'ko' ? '🇷🇺 러시아어 번역:' : '🇰🇷 한국어 번역:'}
                </div>
                <div className="text-gray-800">{translatedTitle}</div>
              </div>
            )}
          </div>
        </div>

        {/* 요약 (선택사항) */}
        <div>
          <label htmlFor="summary" className="block text-sm font-medium text-gray-700 mb-2">
            요약 (선택사항)
          </label>
          <input
            id="summary"
            type="text"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            placeholder="게시글 요약을 입력하세요 (미입력시 자동 생성)"
            maxLength={500}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Rich Text Editor */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            내용 <span className="text-red-500">*</span>
          </label>
          <RichTextEditor
            value={content}
            onChange={setContent}
            placeholder={detectedLang === 'ko' ? '내용을 입력하세요...' : 'Введите содержание...'}
          />
          <div className="mt-2 text-sm text-gray-500">
            💡 이미지/동영상 버튼을 클릭하면 파일을 첨부할 수 있습니다.
          </div>
        </div>

        {/* 태그 */}
        <div>
          <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-2">
            태그 (쉼표로 구분)
          </label>
          <input
            id="tags"
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder={detectedLang === 'ko' ? '예: 공지사항, 이벤트, 뉴스' : 'Например: объявление, событие, новости'}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* 옵션 */}
        <div className="flex items-center gap-4">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={allowComments}
              onChange={(e) => setAllowComments(e.target.checked)}
              className="mr-2 w-4 h-4"
            />
            <span className="text-sm">댓글 허용</span>
          </label>
        </div>

        {/* 버튼 */}
        <div className="flex gap-3 pt-4 border-t">
          <button
            type="submit"
            disabled={isSubmitting || !title.trim() || !content.trim()}
            className="flex-1 px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {isSubmitting ? '작성 중...' : '게시글 등록'}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={isSubmitting}
              className="px-6 py-3 bg-gray-200 text-gray-700 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 transition"
            >
              취소
            </button>
          )}
        </div>
      </form>

      {/* 번역 안내 */}
      {autoTranslate && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
          <h3 className="font-medium text-green-800 mb-2">🌐 자동 번역 기능</h3>
          <ul className="text-sm text-green-700 space-y-1">
            <li>✓ 게시글 등록 시 제목과 내용이 자동으로 번역됩니다</li>
            <li>✓ {detectedLang === 'ko' ? '러시아어' : '한국어'} 사용자도 번역된 내용을 볼 수 있습니다</li>
            <li>✓ DeepL API를 사용하여 고품질 번역을 제공합니다</li>
            <li>✓ 원문 보기/번역 보기 전환이 가능합니다</li>
          </ul>
        </div>
      )}
    </div>
  );
}
