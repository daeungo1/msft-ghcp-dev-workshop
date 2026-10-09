export type Member = {
  id: number;
  name: string;
  role: string;
};

export type Post = {
  id: number;
  author_id: number;
  content: string;
  created_at: string;
};

let currentMemberId: number | null = null;

export function setCurrentMemberId(memberId: number | null) {
  currentMemberId = memberId;
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  if (currentMemberId !== null) {
    headers.set("X-Member-Id", String(currentMemberId));
  }
  const response = await fetch(path, { ...init, headers });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as
      | { error?: { message?: string } }
      | null;
    throw new Error(body?.error?.message ?? "요청을 처리하지 못했습니다.");
  }
  return (await response.json()) as T;
}

export function getMembers() {
  return request<Member[]>("/api/members");
}

export function createMember(name: string) {
  return request<Member>("/api/members", {
    method: "POST",
    body: JSON.stringify({ name }),
  });
}

export function getPosts() {
  return request<Post[]>("/api/posts");
}

export function createPost(content: string) {
  return request<Post>("/api/posts", {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}
