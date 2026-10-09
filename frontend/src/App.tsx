import { useEffect, useMemo, useState } from "react";

import { type Member, getMembers, setCurrentMemberId } from "./api";
import { MemberSelect } from "./components/MemberSelect";
import { PostComposer } from "./components/PostComposer";
import { PostList } from "./components/PostList";

export default function App() {
  const [members, setMembers] = useState<Member[]>([]);
  const [selectedMemberId, setSelectedMemberId] = useState<number | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
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
            <h2>전체 글</h2>
            <button className="ghost-button" type="button" onClick={() => setReloadKey((value) => value + 1)}>
              새로고침
            </button>
          </div>
          {error ? <p className="error-text">{error}</p> : null}
          {selectedMemberId ? (
            <PostList
              key={`${selectedMemberId}-${reloadKey}`}
              authorNames={memberNames}
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
