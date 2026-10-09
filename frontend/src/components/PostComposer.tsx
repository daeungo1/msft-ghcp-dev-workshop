import { FormEvent, useMemo, useState } from "react";

import { createPost } from "../api";

type PostComposerProps = {
  disabled: boolean;
  onCreated: () => void;
  onError: (message: string) => void;
};

export function PostComposer({ disabled, onCreated, onError }: PostComposerProps) {
  const [content, setContent] = useState("");
  const remaining = useMemo(() => 280 - content.length, [content.length]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      await createPost(content.trim());
      setContent("");
      onCreated();
    } catch (reason) {
      onError(reason instanceof Error ? reason.message : "글 작성에 실패했습니다.");
    }
  }

  return (
    <form className="composer" onSubmit={(event) => void handleSubmit(event)}>
      <label className="field">
        <span>내용</span>
        <textarea
          aria-label="게시글 내용"
          maxLength={280}
          rows={4}
          value={content}
          onChange={(event) => setContent(event.target.value)}
          placeholder="지금 공유하고 싶은 내용을 적어 보세요."
        />
      </label>
      <div className="composer-footer">
        <span className={remaining < 20 ? "counter warning" : "counter"}>
          {content.length} / 280
        </span>
        <button type="submit" disabled={disabled || content.trim().length === 0}>
          등록
        </button>
      </div>
    </form>
  );
}
