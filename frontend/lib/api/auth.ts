import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username?: string;
  nickname: string;
  password: string;
  preferred_lang?: 'ko' | 'ru';
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserResponse {
  id: number;
  email: string;
  username?: string;
  nickname: string;
  role: 'user' | 'moderator' | 'admin';
  profile_image?: string;
  preferred_lang: 'ko' | 'ru';
  is_active: boolean;
  is_verified: boolean;
}

/**
 * 로그인
 */
export async function login(credentials: LoginCredentials): Promise<TokenResponse> {
  const response = await axios.post(`${API_URL}/api/auth/email/login`, credentials);
  return response.data;
}

/**
 * 회원가입
 */
export async function register(data: RegisterData): Promise<TokenResponse> {
  const response = await axios.post(`${API_URL}/api/auth/email/register`, data);
  return response.data;
}

/**
 * 현재 사용자 정보 조회
 */
export async function getCurrentUser(accessToken: string): Promise<UserResponse> {
  const response = await axios.get(`${API_URL}/api/users/me`, {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  });
  return response.data;
}

/**
 * 로그아웃
 */
export async function logout(accessToken: string): Promise<void> {
  try {
    await axios.post(
      `${API_URL}/api/auth/logout`,
      {},
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    );
  } catch (error) {
    console.error('로그아웃 API 호출 실패:', error);
  }
}

/**
 * 토큰 갱신
 */
export async function refreshAccessToken(refreshToken: string): Promise<TokenResponse> {
  const response = await axios.post(`${API_URL}/api/auth/refresh`, {
    refresh_token: refreshToken
  });
  return response.data;
}
