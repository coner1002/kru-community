import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Category {
  id: number;
  slug: string;
  name_ko: string;
  name_ru: string;
  description_ko?: string;
  description_ru?: string;
  icon?: string;
  parent_id?: number;
}

/**
 * 카테고리 목록 조회
 */
export async function getCategories(): Promise<Category[]> {
  const response = await axios.get(`${API_URL}/api/categories/`);
  return response.data;
}
