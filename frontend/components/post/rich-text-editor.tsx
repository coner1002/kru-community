'use client';

import React, { useMemo, useRef } from 'react';
import dynamic from 'next/dynamic';
import 'react-quill/dist/quill.snow.css';

// Quill을 동적으로 import (SSR 방지)
const ReactQuill = dynamic(() => import('react-quill'), {
  ssr: false,
  loading: () => <div className="h-64 bg-gray-100 animate-pulse rounded-md"></div>
});

interface RichTextEditorProps {
  value: string;
  onChange: (content: string) => void;
  placeholder?: string;
  onImageUpload?: (file: File) => Promise<string>;
  onVideoUpload?: (file: File) => Promise<string>;
}

export default function RichTextEditor({
  value,
  onChange,
  placeholder = '내용을 입력하세요...',
  onImageUpload,
  onVideoUpload
}: RichTextEditorProps) {
  // 이미지 핸들러
  const imageHandler = () => {
    const url = prompt('이미지 URL을 입력하세요:');
    if (url) {
      // URL이 제공된 경우 onChange를 통해 이미지 삽입
      const imageTag = `<img src="${url}" alt="image" />`;
      onChange(value + imageTag);
    }
  };

  // 동영상 핸들러
  const videoHandler = () => {
    const url = prompt('동영상 URL을 입력하세요 (YouTube, Vimeo 등):');
    if (url) {
      // URL이 제공된 경우 onChange를 통해 비디오 삽입
      const videoTag = `<iframe src="${url}" frameborder="0" allowfullscreen></iframe>`;
      onChange(value + videoTag);
    }
  };

  // Quill 모듈 설정
  const modules = useMemo(() => ({
    toolbar: {
      container: [
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [{ 'font': [] }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
        [{ 'align': [] }],
        ['blockquote', 'code-block'],
        ['link', 'image', 'video'],
        ['clean']
      ],
      handlers: {
        image: imageHandler,
        video: videoHandler
      }
    },
    clipboard: {
      matchVisual: false
    }
  }), []);

  // Quill 포맷 설정
  const formats = [
    'header', 'font', 'size',
    'bold', 'italic', 'underline', 'strike',
    'color', 'background',
    'script',
    'list', 'bullet', 'indent',
    'align',
    'blockquote', 'code-block',
    'link', 'image', 'video'
  ];

  return (
    <div className="rich-text-editor">
      <ReactQuill
        theme="snow"
        value={value}
        onChange={onChange}
        modules={modules}
        formats={formats}
        placeholder={placeholder}
        className="bg-white"
      />

      <style jsx global>{`
        .rich-text-editor .quill {
          background: white;
          border-radius: 0.375rem;
        }

        .rich-text-editor .ql-toolbar {
          border-top-left-radius: 0.375rem;
          border-top-right-radius: 0.375rem;
          background: #f9fafb;
          border-color: #d1d5db;
        }

        .rich-text-editor .ql-container {
          border-bottom-left-radius: 0.375rem;
          border-bottom-right-radius: 0.375rem;
          border-color: #d1d5db;
          font-size: 1rem;
          font-family: inherit;
        }

        .rich-text-editor .ql-editor {
          min-height: 300px;
          max-height: 600px;
          overflow-y: auto;
        }

        .rich-text-editor .ql-editor.ql-blank::before {
          color: #9ca3af;
          font-style: normal;
        }

        /* 한글 및 키릴 문자 지원 */
        .rich-text-editor .ql-editor {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
            'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
            sans-serif, 'PT Sans', 'Noto Sans KR';
        }

        /* 툴바 버튼 스타일 개선 */
        .rich-text-editor .ql-toolbar button:hover,
        .rich-text-editor .ql-toolbar button:focus {
          color: #2563eb;
        }

        .rich-text-editor .ql-toolbar button.ql-active {
          color: #2563eb;
        }

        /* 이미지 스타일 */
        .rich-text-editor .ql-editor img {
          max-width: 100%;
          height: auto;
          border-radius: 0.375rem;
          margin: 0.5rem 0;
        }

        /* 동영상 스타일 */
        .rich-text-editor .ql-editor video {
          max-width: 100%;
          height: auto;
          border-radius: 0.375rem;
          margin: 0.5rem 0;
        }
      `}</style>
    </div>
  );
}
