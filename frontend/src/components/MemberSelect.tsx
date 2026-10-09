import { FormEvent, useState } from "react";

import { createMember, type Member } from "../api";

type MemberSelectProps = {
  members: Member[];
  selectedMemberId: number | null;
  onSelect: (memberId: number | null) => void;
  onCreated: (member: Member) => void;
};

export function MemberSelect({
  members,
  selectedMemberId,
  onSelect,
  onCreated,
}: MemberSelectProps) {
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      const member = await createMember(name.trim());
      onCreated(member);
      setName("");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "회원 생성에 실패했습니다.");
    }
  }

  return (
    <div className="member-select">
      <label className="field">
        <span>현재 회원</span>
        <select
          aria-label="현재 회원"
          value={selectedMemberId ?? ""}
          onChange={(event) =>
            onSelect(event.target.value === "" ? null : Number(event.target.value))
          }
        >
          <option value="">선택하세요</option>
          {members.map((member) => (
            <option key={member.id} value={member.id}>
              {member.name}
            </option>
          ))}
        </select>
      </label>
      <form className="inline-form" onSubmit={(event) => void handleSubmit(event)}>
        <label className="field grow">
          <span>새 회원</span>
          <input
            aria-label="새 회원 이름"
            maxLength={30}
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="이름을 입력하세요"
          />
        </label>
        <button type="submit">가입</button>
      </form>
      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}
