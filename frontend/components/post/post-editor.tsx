'use client';

import React, { useState, useEffect } from 'react';
import { createPost, PostCreate, detectLanguage } from '@/lib/api/posts';

interface PostEditorProps {
  categoryId: number;
  onSuccess?: (postId: number) => void;
  onCancel?: () => void;
}

export default function PostEditor({ categoryId, onSuccess, onCancel }: PostEditorProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [summary, setSummary] = useState('');
  const [tags, setTags] = useState('');
  const [allowComments, setAllowComments] = useState(true);
  const [autoTranslate, setAutoTranslate] = useState(true);
  const [detectedLang, setDetectedLang] = useState<'ko' | 'ru'>('ko');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [translationPreview, setTranslationPreview] = useState(false);

  // 언어 자동 감지
  useEffect(() => {
    if (title || content) {
      const textToCheck = title + ' ' + content;
      const detected = detectLanguage(textToCheck);
      if (detected === 'ko' || detected === 'ru') {
        setDetectedLang(detected);
      }
    }
  }, [title, content]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const postData: PostCreate = {
        title: title.trim(),
        content: content.trim(),
        summary: summary.trim() || undefined,
        category_id: categoryId,
        tags: tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        allow_comments: allowComments,
        source_lang: detectedLang,
        auto_translate: autoTranslate,
      };

      const result = await createPost(postData);

      if (onSuccess) {
        onSuccess(result.id);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '게시글 작성 중 오류가 발생했습니다.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">새 게시글 작성</h2>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {/* 언어 감지 표시 */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
        <div className="flex items-center justify-between">
          <div>
            <span className="font-medium">감지된 언어: </span>
            <span className="text-blue-700 font-bold">
              {detectedLang === 'ko' ? '🇰🇷 한국어' : '🇷🇺 러시아어'}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <label className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={autoTranslate}
                onChange={(e) => setAutoTranslate(e.target.checked)}
                className="mr-2"
              />
              <span className="text-sm">
                {detectedLang === 'ko' ? '러시아어로 자동 번역' : '한국어로 자동 번역'}
              </span>
            </label>
          </div>
        </div>
        {autoTranslate && (
          <div className="mt-2 text-sm text-gray-600">
            ℹ️ DeepL API를 사용하여 자동으로 번역됩니다.
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* 제목 */}
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            제목 <span className="text-red-500">*</span>
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="게시글 제목을 입력하세요"
            required
            maxLength={255}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* 요약 */}
        <div>
          <label htmlFor="summary" className="block text-sm font-medium text-gray-700 mb-1">
            요약 (선택사항)
          </label>
          <input
            id="summary"
            type="text"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            placeholder="게시글 요약을 입력하세요"
            maxLength={500}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* 내용 */}
        <div>
          <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">
            내용 <span className="text-red-500">*</span>
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="게시글 내용을 입력하세요"
            required
            rows={12}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-vertical"
          />
        </div>

        {/* 태그 */}
        <div>
          <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-1">
            태그 (쉼표로 구분)
          </label>
          <input
            id="tags"
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="예: 공지사항, 이벤트, 뉴스"
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
              className="mr-2"
            />
            <span className="text-sm">댓글 허용</span>
          </label>
        </div>

        {/* 버튼 */}
        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? '작성 중...' : '게시글 작성'}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={isSubmitting}
              className="px-6 py-3 bg-gray-200 text-gray-700 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50"
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
            <li>✓ 게시글 작성 시 자동으로 {detectedLang === 'ko' ? '러시아어' : '한국어'}로 번역됩니다</li>
            <li>✓ DeepL API를 사용하여 고품질 번역을 제공합니다</li>
            <li>✓ 양쪽 언어 사용자 모두 게시글을 읽을 수 있습니다</li>
          </ul>
        </div>
      )}
    </div>
  );
}
