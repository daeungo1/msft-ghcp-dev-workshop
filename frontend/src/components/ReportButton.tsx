import { FormEvent, useState } from "react";

import { createReport } from "../api";

type ReportButtonProps = {
  postId: number;
  onError: (message: string) => void;
};

export function ReportButton({ postId, onError }: ReportButtonProps) {
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      await createReport(postId, reason.trim());
      setReason("");
      setOpen(false);
      onError("");
    } catch (reasonError) {
      onError(reasonError instanceof Error ? reasonError.message : "신고에 실패했습니다.");
    }
  }

  if (!open) {
    return (
      <button className="ghost-button small-button" type="button" onClick={() => setOpen(true)}>
        신고
      </button>
    );
  }

  return (
    <form className="report-inline" onSubmit={(event) => void handleSubmit(event)}>
      <input
        aria-label={`신고 사유 ${postId}`}
        maxLength={200}
        value={reason}
        onChange={(event) => setReason(event.target.value)}
        placeholder="사유를 입력하세요"
      />
      <button className="small-button" type="submit" disabled={reason.trim().length === 0}>
        제출
      </button>
      <button
        className="ghost-button small-button"
        type="button"
        onClick={() => {
          setOpen(false);
          setReason("");
        }}
      >
        취소
      </button>
    </form>
  );
}
