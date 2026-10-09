import { useEffect, useState } from "react";

import { type Post, getPosts } from "../api";

type PostListProps = {
  authorNames: Record<number, string>;
  onError: (message: string) => void;
};

export function PostList({ authorNames, onError }: PostListProps) {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    void getPosts()
      .then((items) => {
        setPosts(items);
        onError("");
      })
      .catch((reason: Error) => onError(reason.message));
  }, [onError]);

  if (posts.length === 0) {
    return <p className="empty-text">아직 글이 없습니다.</p>;
  }

  return (
    <ul className="feed-list">
      {posts.map((post) => (
        <li key={post.id} className="feed-card">
          <div className="feed-meta">
            <strong>{authorNames[post.author_id] ?? `회원 #${post.author_id}`}</strong>
            <span>{new Date(post.created_at).toLocaleString("ko-KR")}</span>
          </div>
          <p>{post.content}</p>
        </li>
      ))}
    </ul>
  );
}
