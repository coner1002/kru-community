import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface PostCreate {
  title: string;
  content: string;
  summary?: string;
  category_id: number;
  tags?: string[];
  images?: string[];
  attachments?: any[];
  allow_comments?: boolean;
  source_lang: 'ko' | 'ru';
  auto_translate?: boolean;
}

export interface PostResponse {
  id: number;
  user_id: number;
  category_id: number;
  title: string;
  content: string;
  summary?: string;
  source_lang: string;

  // 번역된 내용
  translated_title_ko?: string;
  translated_title_ru?: string;
  translated_content_ko?: string;
  translated_content_ru?: string;
  translated_summary_ko?: string;
  translated_summary_ru?: string;
  auto_translated: boolean;

  // 메타데이터
  slug: string;
  status: string;
  tags: string[];
  images: string[];
  is_pinned: boolean;
  is_featured: boolean;
  allow_comments: boolean;

  // 통계
  view_count: number;
  like_count: number;
  comment_count: number;
  share_count: number;

  // 타임스탬프
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface PostListResponse {
  items: PostResponse[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/**
 * 게시글 생성 (자동 번역 포함)
 */
export async function createPost(postData: PostCreate): Promise<PostResponse> {
  const response = await axios.post(`${API_URL}/api/posts/`, postData);
  return response.data;
}

/**
 * 게시글 목록 조회
 */
export async function getPosts(params: {
  page?: number;
  page_size?: number;
  category_id?: number;
  status_filter?: string;
} = {}): Promise<PostListResponse> {
  const response = await axios.get(`${API_URL}/api/posts/`, { params });
  return response.data;
}

/**
 * 게시글 상세 조회
 */
export async function getPost(postId: number): Promise<PostResponse> {
  const response = await axios.get(`${API_URL}/api/posts/${postId}`);
  return response.data;
}

/**
 * 게시글 수정
 */
export async function updatePost(
  postId: number,
  postData: Partial<PostCreate>
): Promise<PostResponse> {
  const response = await axios.put(`${API_URL}/api/posts/${postId}`, postData);
  return response.data;
}

/**
 * 게시글 삭제
 */
export async function deletePost(postId: number): Promise<void> {
  await axios.delete(`${API_URL}/api/posts/${postId}`);
}

/**
 * 언어 감지 (간단한 휴리스틱)
 */
export function detectLanguage(text: string): 'ko' | 'ru' | 'en' {
  // 한글 감지
  if (/[\uAC00-\uD7AF]/.test(text)) {
    return 'ko';
  }
  // 키릴 문자 감지
  if (/[\u0400-\u04FF]/.test(text)) {
    return 'ru';
  }
  return 'en';
}
