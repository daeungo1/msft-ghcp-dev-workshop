import { useEffect, useState } from "react";

import { followMember, type Post, getPosts, unfollowMember } from "../api";

type PostListProps = {
  authorNames: Record<number, string>;
  currentMemberId: number;
  followingIds: number[];
  onFollowChange: (targetId: number, nextIsFollowing: boolean) => void;
  onError: (message: string) => void;
};

export function PostList({
  authorNames,
  currentMemberId,
  followingIds,
  onFollowChange,
  onError,
}: PostListProps) {
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

  async function handleFollow(targetId: number, isFollowing: boolean) {
    try {
      if (isFollowing) {
        await unfollowMember(targetId);
      } else {
        await followMember(targetId);
      }
      onFollowChange(targetId, !isFollowing);
      onError("");
    } catch (reason) {
      onError(reason instanceof Error ? reason.message : "팔로우 처리에 실패했습니다.");
    }
  }

  return (
    <ul className="feed-list">
      {posts.map((post) => (
        <li key={post.id} className="feed-card">
          <div className="feed-meta">
            <strong>{authorNames[post.author_id] ?? `회원 #${post.author_id}`}</strong>
            <div className="meta-actions">
              {post.author_id !== currentMemberId ? (
                <button
                  className="ghost-button small-button"
                  type="button"
                  onClick={() =>
                    void handleFollow(post.author_id, followingIds.includes(post.author_id))
                  }
                >
                  {followingIds.includes(post.author_id) ? "언팔로우" : "팔로우"}
                </button>
              ) : null}
              <span>{new Date(post.created_at).toLocaleString("ko-KR")}</span>
            </div>
          </div>
          <p>{post.content}</p>
        </li>
      ))}
    </ul>
  );
}
