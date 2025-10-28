'use client';

import React, { useState } from 'react';
import { PostResponse } from '@/lib/api/posts';

interface PostViewProps {
  post: PostResponse;
  userLanguage?: 'ko' | 'ru';
  currentUser?: {
    id: number;
    role: 'user' | 'moderator' | 'admin';
  } | null;
  categorySlug?: string;
}

export default function PostView({ post, userLanguage = 'ko', currentUser = null, categorySlug }: PostViewProps) {
  const [showOriginal, setShowOriginal] = useState(false);

  // 공지사항 여부 확인
  const isNotice = categorySlug === 'notice';

  // 권한 확인
  const isAdmin = currentUser?.role === 'admin' || currentUser?.role === 'moderator';
  const isAuthor = currentUser?.id === post.user_id;
  const canEdit = isAdmin || (isAuthor && !isNotice);
  const canDelete = isAdmin || (isAuthor && !isNotice);
  const canComment = !isNotice || isAdmin;

  // 사용자 언어에 맞는 번역된 내용 가져오기
  const getTranslatedContent = () => {
    if (showOriginal) {
      return {
        title: post.title,
        content: post.content,
        summary: post.summary,
        lang: post.source_lang,
      };
    }

    if (userLanguage === 'ko') {
      return {
        title: post.translated_title_ko || post.title,
        content: post.translated_content_ko || post.content,
        summary: post.translated_summary_ko || post.summary,
        lang: 'ko',
      };
    } else {
      return {
        title: post.translated_title_ru || post.title,
        content: post.translated_content_ru || post.content,
        summary: post.translated_summary_ru || post.summary,
        lang: 'ru',
      };
    }
  };

  const displayContent = getTranslatedContent();
  const isTranslated = post.auto_translated && !showOriginal && displayContent.lang !== post.source_lang;

  return (
    <article className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      {/* 헤더 */}
      <header className="mb-6 pb-4 border-b">
        <h1 className="text-3xl font-bold mb-3">{displayContent.title}</h1>

        {/* 메타 정보 */}
        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
          <div className="flex items-center gap-2">
            <span>👤 작성자</span>
            <span className="font-medium">User #{post.user_id}</span>
          </div>
          <div className="flex items-center gap-2">
            <span>📅</span>
            <time>{new Date(post.created_at).toLocaleDateString()}</time>
          </div>
          <div className="flex items-center gap-2">
            <span>👁️</span>
            <span>{post.view_count} 조회</span>
          </div>
          <div className="flex items-center gap-2">
            <span>💬</span>
            <span>{post.comment_count} 댓글</span>
          </div>
        </div>

        {/* 번역 상태 표시 */}
        {post.auto_translated && (
          <div className="mt-3 flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm">
              {isTranslated ? (
                <div className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
                  🌐 자동 번역됨 ({post.source_lang === 'ko' ? '한국어' : '러시아어'} → {displayContent.lang === 'ko' ? '한국어' : '러시아어'})
                </div>
              ) : (
                <div className="px-3 py-1 bg-green-100 text-green-700 rounded-full">
                  📝 원문 ({post.source_lang === 'ko' ? '한국어' : '러시아어'})
                </div>
              )}
            </div>
            <button
              onClick={() => setShowOriginal(!showOriginal)}
              className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition"
            >
              {showOriginal ? '번역 보기' : '원문 보기'}
            </button>
          </div>
        )}

        {/* 태그 */}
        {post.tags && post.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {post.tags.map((tag, index) => (
              <span
                key={index}
                className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-md"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}
      </header>

      {/* 요약 */}
      {displayContent.summary && (
        <div className="mb-6 p-4 bg-gray-50 border-l-4 border-blue-500 rounded-r-md">
          <p className="text-gray-700 font-medium">{displayContent.summary}</p>
        </div>
      )}

      {/* 본문 */}
      <div className="prose max-w-none mb-6">
        <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
          {displayContent.content}
        </div>
      </div>

      {/* 이미지 */}
      {post.images && post.images.length > 0 && (
        <div className="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          {post.images.map((image, index) => (
            <img
              key={index}
              src={image}
              alt={`Image ${index + 1}`}
              className="rounded-lg w-full h-auto"
            />
          ))}
        </div>
      )}

      {/* 푸터 - 통계 및 액션 버튼 */}
      <footer className="mt-8 pt-4 border-t">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            {/* 추천 버튼 (모든 사용자) */}
            <button className="flex items-center gap-1 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition">
              <span>👍</span>
              <span>{post.like_count}</span>
            </button>

            {/* 댓글 버튼 (공지사항이 아니거나 관리자인 경우) */}
            {canComment && (
              <button className="flex items-center gap-1 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition">
                <span>💬</span>
                <span>댓글 {post.comment_count}</span>
              </button>
            )}

            {/* 공유 버튼 (모든 사용자) */}
            <button className="flex items-center gap-1 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition">
              <span>🔗</span>
              <span>공유 {post.share_count}</span>
            </button>
          </div>

          {isTranslated && (
            <div className="text-xs text-gray-500">
              Translated by DeepL API
            </div>
          )}
        </div>

        {/* 관리 버튼 (권한이 있는 경우) */}
        {currentUser && (canEdit || canDelete) && (
          <div className="flex items-center gap-2 pt-4 border-t">
            {canEdit && (
              <button className="px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-md transition">
                ✏️ 수정
              </button>
            )}
            {canDelete && (
              <button className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition">
                🗑️ 삭제
              </button>
            )}
            {!isNotice && (
              <button className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-md transition">
                🚨 신고
              </button>
            )}
          </div>
        )}

        {/* 공지사항 안내 */}
        {isNotice && !isAdmin && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md text-sm text-blue-700">
            ℹ️ 공지사항은 조회 및 추천, 공유만 가능합니다.
          </div>
        )}
      </footer>
    </article>
  );
}
