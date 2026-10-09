import { useEffect, useMemo, useState } from "react";

import { getFollowing, type Member, getMembers, setCurrentMemberId } from "./api";
import { Feed } from "./components/Feed";
import { MemberSelect } from "./components/MemberSelect";
import { PostComposer } from "./components/PostComposer";

export default function App() {
  const [members, setMembers] = useState<Member[]>([]);
  const [selectedMemberId, setSelectedMemberId] = useState<number | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [followingIds, setFollowingIds] = useState<number[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    void getMembers()
      .then((items) => {
        setMembers(items);
        if (items.length > 0) {
          setSelectedMemberId((current) => current ?? items[0].id);
        }
      })
      .catch((reason: Error) => setError(reason.message));
  }, []);

  useEffect(() => {
    setCurrentMemberId(selectedMemberId);
    if (selectedMemberId === null) {
      setFollowingIds([]);
      return;
    }
    void getFollowing(selectedMemberId)
      .then((items) => setFollowingIds(items.map((member) => member.id)))
      .catch((reason: Error) => setError(reason.message));
  }, [selectedMemberId]);

  const memberNames = useMemo(
    () => Object.fromEntries(members.map((member) => [member.id, member.name])),
    [members],
  );

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">사내 미니 SNS</p>
          <h1>TeamFeed</h1>
        </div>
        <MemberSelect
          members={members}
          selectedMemberId={selectedMemberId}
          onSelect={(value) => setSelectedMemberId(value)}
          onCreated={(member) => {
            setMembers((current) => [...current, member]);
            setSelectedMemberId(member.id);
            setError("");
          }}
        />
      </header>
      <main className="content-grid">
        <section className="panel">
          <h2>새 글 쓰기</h2>
          <PostComposer
            disabled={!selectedMemberId}
            onCreated={() => {
              setReloadKey((value) => value + 1);
              setError("");
            }}
            onError={setError}
          />
        </section>
        <section className="panel">
          <div className="panel-header">
            <h2>피드</h2>
            <button className="ghost-button" type="button" onClick={() => setReloadKey((value) => value + 1)}>
              새로고침
            </button>
          </div>
          {error ? <p className="error-text">{error}</p> : null}
          {selectedMemberId ? (
              <Feed
              key={`${selectedMemberId}-${reloadKey}`}
              authorNames={memberNames}
              currentMemberId={selectedMemberId}
              followingIds={followingIds}
              onFollowChange={(targetId, nextIsFollowing) =>
                setFollowingIds((current) =>
                  nextIsFollowing
                    ? [...new Set([...current, targetId])].sort((a, b) => a - b)
                    : current.filter((id) => id !== targetId),
                )
              }
              onError={setError}
            />
          ) : (
            <p className="empty-text">먼저 회원을 선택하거나 가입해 주세요.</p>
          )}
        </section>
      </main>
    </div>
  );
}
