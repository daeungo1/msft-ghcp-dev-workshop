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

export type FeedPage = {
  items: Post[];
  next_before: number | null;
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
  const text = await response.text();
  return (text ? (JSON.parse(text) as T) : undefined) as T;
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

export function getFeed(before?: number | null) {
  const search = new URLSearchParams({ limit: "20" });
  if (before) {
    search.set("before", String(before));
  }
  return request<FeedPage>(`/api/feed?${search.toString()}`);
}

export function createPost(content: string) {
  return request<Post>("/api/posts", {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}

export function getFollowing(memberId: number) {
  return request<Member[]>(`/api/members/${memberId}/following`);
}

export function followMember(targetId: number) {
  return request<void>(`/api/follows/${targetId}`, {
    method: "POST",
    body: JSON.stringify({}),
  });
}

export function unfollowMember(targetId: number) {
  return request<void>(`/api/follows/${targetId}`, {
    method: "DELETE",
  });
}
